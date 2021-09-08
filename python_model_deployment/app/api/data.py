#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


import math
import numpy as np
import pandas as pd
import os
import shutil
import weakref
from datetime import datetime as dt
from joblib import load
from flask import (current_app as app)
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
from sklearn.metrics import confusion_matrix

from app.api.errors import bad_request


# file remover for temp files sent by the api
class FileRemover(object):
    def __init__(self):
        self.weak_references = dict()  # weak_ref -> filepath to remove

    def cleanup_once_done(self, response, filepath):
        wr = weakref.ref(response, self._do_cleanup)
        self.weak_references[wr] = filepath

    def _do_cleanup(self, wr):
        filepath = self.weak_references[wr]
        # print(f'Deleting {filepath}')
        shutil.rmtree(filepath, ignore_errors=True)


# get a mongo collection
def get_mongo_collection(database, collection):
    """Gets and returns a mongo collection."""

    client = MongoClient(os.getenv('MONGO_URI'))
    db = client[database]
    col = db[collection]
    return col


# extract json from request
# TODO: modify this to use a key to extract dict items
# TODO: setup api to use very specific key names (new_data, api_key, labels)
def extract_json_from_request(request_data):
    if isinstance(request_data, str):
        try:
            request_data = eval(request_data)
        except NameError:
            return request_data
    if isinstance(request_data, dict) and len(request_data) == 1:
        for key, value in request_data.items():
            request_data = value
        if isinstance(request_data, str):
            try:
                request_data = eval(request_data)
            except NameError:
                return request_data
    return request_data


# generate predictions from new data
def generate_predictions(new_data):
    """This function receives new data, performs data validation, then generates predictions using the ML model."""

    # if isinstance(new_data, str):
    #     new_data = eval(new_data)
    # if isinstance(new_data, dict) and len(new_data) == 1:
    #     for key, value in new_data.items():
    #         new_data = value
    #     if isinstance(new_data, str):
    #         new_data = eval(new_data)

    new_data = extract_json_from_request(new_data)

    if isinstance(new_data, list):
        new_data = np.array(new_data)

    try:
        if not new_data.shape == (4,):
            if not new_data.shape[1] == 4:
                return bad_request(
                    '''Supplied data was not in the correct format, expected new_data to be np.ndarray or a list, '''
                    f'''received {type(new_data)}'''
                )
    except AttributeError:
        return bad_request(
            '''Supplied data was not in the correct format, expected new_data to be np.ndarray or a list, '''
            f'''received {type(new_data)}'''
        )

    if not isinstance(new_data, np.ndarray):
        return bad_request(
            '''Supplied data was not in the correct format, expected new_data to be np.ndarray or a list, '''
            f'''received {type(new_data)}'''
        )

    if new_data.shape == (4,):
        new_data = new_data.reshape(1, -1)

    knn = load(''.join([app.config['APPLICATION_HOME'], '/app/static/model/iris_knn.joblib']))

    target_names = ['setosa', 'versicolor', 'virginica']

    raw_predictions = knn.predict(new_data)
    target_predictions = [target_names[i] for i in raw_predictions]

    mongo_write_data = [
        {
            'data': list(new_data[idx]),
            'prediction': value,
            'timestamp': dt.now()
        } for idx, value in enumerate(target_predictions)
    ]

    # predictions = [{idx: target_names[value]} for idx, value in enumerate(raw_predictions)]
    # if len(predictions) == 1:
    #     predictions = predictions[0]

    # write the predictions to the mongo collection
    col = get_mongo_collection(database=app.config.get('DATABASE'), collection=app.config.get('PREDICTION_COLLECTION'))
    result = col.insert_many(mongo_write_data)

    inserted_ids = result.inserted_ids

    docs = col.find({'_id': {'$in': inserted_ids}})
    docs = [doc for doc in docs]
    for doc in docs:
        doc['_id'] = str(doc['_id'])

    return docs


# label data that already has predictions
def label_predictions(data):
    """This function accepts labeled data and adds the correct label to the mongo collection.

    :param data: must be a list of dictionaries with keys of '_id' and 'label'. '_id' is the Object id as a string
    that identifies a document in mongo to update, and 'label' is the user assigned correct label for the data.
    """

    # if isinstance(data, str):
    #     data = eval(data)
    # if isinstance(data, dict) and len(data) == 1:
    #     for key, value in data.items():
    #         data = value
    #     if isinstance(data, str):
    #         data = eval(data)
    # if isinstance(data, dict):
    #     data = [data]

    data = extract_json_from_request(data)

    if not isinstance(data, list) or not all([isinstance(i, dict) for i in data]):
        return bad_request(f'Supplied data was not in the correct format. data must be a list of dictionaries.')

    if not all(['_id' in record.keys() for record in data]) and all(['label' in record.keys() for record in data]):
        return bad_request(f'All records must contain an "_id" and a "label".')

    ids = [record['_id'] for record in data]
    labels = [record['label'] for record in data]
    if not all([isinstance(i, str) for i in ids]) and not all([isinstance(label, str) for label in labels]):
        return bad_request(f'All "_id" and "label" values must be strings.')
    if not all([label.lower() in ['setosa', 'versicolor', 'virginica'] for label in labels]):
        return bad_request(f'Only "setosa", "versicolor", or "virginica" are allowed as label values.')

    updated_ids = []
    invalid_ids = []
    col = get_mongo_collection(database=app.config.get('DATABASE'), collection=app.config.get('PREDICTION_COLLECTION'))
    for record in data:
        try:
            result = col.update_one(
                # filter parameter
                {'_id': ObjectId(record['_id'])},
                # set the label
                {'$set': {'label': record['label'].lower()}},
                upsert=False
            )
            if result.matched_count != 1:
                invalid_ids.append(record['_id'])
            else:
                updated_ids.append(record['_id'])
        except InvalidId:
            invalid_ids.append(record['_id'])

    if invalid_ids:
        message = f'only {len(updated_ids)} records labeled. invalid ids supplied: {[i for i in invalid_ids]}'
    else:
        message = f'{len(updated_ids)} records labeled'

    label_result = {'label_result': message}

    return label_result


# retrieve most recent model performance metrics
def get_latest_perf_metrics(collection):
    docs = collection.find({}).sort('timestamp', pymongo.DESCENDING).limit(1)
    doc = [doc for doc in docs][0]
    del doc['_id']
    return doc


# custom date string format exception
class IncorrectDateFormat(ValueError):
    def __init__(self, date_string):
        self.date_string = date_string
        self.message = f'date string {date_string} must be in format "YYYY-MM-DD"'
        super().__init__(self.message)


# Generate model performance metrics
# edit the function to query labeled records from mongo for performance metrics
def get_model_performance(collection, mode='all', start_date=None, end_date=None, pct=None, count=None):
    """Query labeled data only from the iris_knn predictions collection in MongoDB.

    collection: Mongo collection: the mongo collection with the model performance metrics
    mode: str: either 'all', 'dates', 'pct', or 'count'. if mode=='dates', specify a date range using start_date
               and end date.
    start_date: datetime: required if mode=='dates' else not used (inclusive of start_date)
    end_date: datetime: required if mode=='dates' else not used (inclusive of end_date)
    pct: float: decimal percent for the percent of labeled records to use for model performance metrics
    count: int: number of labeled documents to use for model performance metrics
    """

    if mode == 'all':
        params = {}
        criteria = 'all records'
    elif mode == 'dates':
        if not start_date or not end_date:
            raise ValueError('start_date and end_date are required when mode="dates"')
        if not isinstance(start_date, str) or not isinstance(end_date, str):
            raise TypeError('start_date and end_date must be supplied as strings in format "YYYY-MM-DD"')
        try:
            start_date = dt.strptime(start_date, '%Y-%m-%d')
            end_date = dt.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise IncorrectDateFormat

        params = {
            '$and':
                [
                    {'timestamp': {'$gte': start_date}},
                    {'timestamp': {'$lte': end_date}}
                ]
        }
        criteria = {'start_date': start_date, 'end_date': end_date}
    elif mode == 'pct':
        if not pct:
            raise ValueError('pct is required when mode="pct"')
        if not isinstance(pct, int) and not isinstance(pct, float):
            raise TypeError('pct must be a decimal number between 0-1 (30% should be supplied as 0.3)')
        if 1 < pct < 0:
            raise ValueError('pct must be a decimal number between 0-1 (30% should be supplied as 0.3)')
        params = {}
        criteria = {'pct': pct}
    elif mode == 'count':
        if not count:
            raise ValueError('count is required when mode="count"')
        if not isinstance(count, int):
            raise TypeError('count must be supplied as an integer')
        params = {}
        criteria = {'count': count}
    else:
        raise ValueError('mode must be either "all", "dates", "pct", or "count"')

    params['label'] = {'$exists': True, '$ne': None}

    # pred_col = get_mongo_collection(database='pocMLModelMonitoring', collection='iris_knn')

    pred_docs = collection.find(params, {'prediction': 1, 'label': 1}).sort('prediction_timestamp', pymongo.DESCENDING)
    pred_docs = [doc for doc in pred_docs]

    if mode == 'pct':
        num_docs = math.ceil(len(pred_docs) * pct)
        pred_docs = pred_docs[:num_docs]
    elif mode == 'count':
        if count < len(pred_docs):
            pred_docs = pred_docs[:count]
        else:
            # if count is greater than the number of docs, include this in the criteria
            criteria = {'count': count, 'found': len(pred_docs)}

    if not pred_docs:
        # exit the function if nothing is found
        return

    dff = pd.DataFrame(pred_docs)

    target_names = ['setosa', 'versicolor', 'virginica']

    # calculate the confusion matrix
    # adding the labels ensures the correct index order for the species
    conf_matrix = confusion_matrix(dff['label'], dff['prediction'], labels=target_names)

    # model accuracy
    accuracy = np.sum([conf_matrix[i][i] for i in range(conf_matrix.shape[0])]) / np.sum(conf_matrix)

    # precision, recall, and f1 scores
    precision = {}
    recall = {}
    f1 = {}

    targets_found = sorted(list(dff['label'].unique()))

    if 'setosa' in targets_found:
        precision['setosa'] = conf_matrix[0][0] / np.sum(conf_matrix[:, 0])
        recall['setosa'] = conf_matrix[0][0] / np.sum(conf_matrix[0])
        f1['setosa'] = 2 * (precision['setosa'] * recall['setosa']) / (precision['setosa'] + recall['setosa'])
    else:
        precision['setosa'] = None
        recall['setosa'] = None
        f1['setosa'] = None

    if 'versicolor' in targets_found:
        precision['versicolor'] = conf_matrix[1][1] / np.sum(conf_matrix[:, 1])
        recall['versicolor'] = conf_matrix[1][1] / np.sum(conf_matrix[1])
        f1['versicolor'] = 2 * (precision['versicolor'] * recall['versicolor']) / (
                    precision['versicolor'] + recall['versicolor'])
    else:
        precision['versicolor'] = None
        recall['versicolor'] = None
        f1['versicolor'] = None

    if 'virginica' in targets_found:
        precision['virginica'] = conf_matrix[2][2] / np.sum(conf_matrix[:, 2])
        recall['virginica'] = conf_matrix[2][2] / np.sum(conf_matrix[2])
        f1['virginica'] = 2 * (precision['virginica'] * recall['virginica']) / (
                    precision['virginica'] + recall['virginica'])
    else:
        precision['virginica'] = None
        recall['virginica'] = None
        f1['virginica'] = None

    sample_size = int(np.sum(conf_matrix))

    class_balance = {}
    for species in target_names:
        if species not in targets_found:
            class_balance[species] = 0.0
        else:
            class_balance[species] = dff['label'].value_counts()[species] / dff.shape[0]

    #     # get the mongo collection
    #     col = get_mongo_collection(database='pocMLModelMonitoring', collection='irisKnnPerformance')

    # synthesize the observation
    document = {
        'timestamp': dt.now(),
        'measurement_mode': mode,
        'query_criteria': criteria,
        'model_accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'F1': f1,
        'class_balance': class_balance,
        'sample_size': sample_size
    }

    #     # write the data
    #     result = col.insert_one(document)

    # return the result object
    # return result

    return document
