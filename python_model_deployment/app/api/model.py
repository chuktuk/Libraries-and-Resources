#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

from app.api import bp
from app.api.errors import bad_request, error_response
from app.api import data
from flask import jsonify, redirect, request, send_file, url_for, current_app as app

from joblib import load
import numpy as np
import json
import tempfile


# create a file_remover object
file_remover = data.FileRemover()


# TODO: add ability to upload file instead of passing json for batch loads
# TODO: though this could be handled by the other end of the api that makes the call


# when registering the blueprint in app/__init__.py all routes are prefixed with '/api'


# predictions
@bp.route('/model/predict', methods=['POST'])
def get_predict():

    new_data = request.get_json()

    docs = data.generate_predictions(new_data)
    for doc in docs:
        doc['prediction_timestamp'] = doc['prediction_timestamp'].strftime('%Y-%m-%d %H:%M:%S')

    # send temp file
    tempdir = tempfile.mkdtemp()
    filepath = ''.join([tempdir, '/predictions.json'])
    with open(filepath, 'w') as file:
        json.dump(docs, file)
    resp = send_file(filepath)
    file_remover.cleanup_once_done(resp, tempdir)
    return resp

    # consider returning a file instead
    # return jsonify(docs)

    # if isinstance(new_data, dict) and len(new_data) == 1:
    #     for key, value in new_data.items():
    #         new_data = value
    #     if isinstance(new_data, str):
    #         new_data = eval(new_data)
    #
    # if isinstance(new_data, list):
    #     new_data = np.array(new_data)
    #
    # try:
    #     if not new_data.shape == (4,):
    #         if not new_data.shape[1] == 4:
    #             return bad_request(
    #                 '''Supplied data was not in the correct format, expected new_data to be np.ndarray or a list, '''
    #                 f'''received {type(new_data)}'''
    #             )
    # except AttributeError:
    #     return bad_request(
    #         '''Supplied data was not in the correct format, expected new_data to be np.ndarray or a list, '''
    #         f'''received {type(new_data)}'''
    #     )
    #
    # if not isinstance(new_data, np.ndarray):
    #     return bad_request(
    #         '''Supplied data was not in the correct format, expected new_data to be np.ndarray or a list, '''
    #         f'''received {type(new_data)}'''
    #     )
    #
    # if new_data.shape == (4,):
    #     new_data = new_data.reshape(1, -1)
    #
    # knn = load(''.join([app.config['APPLICATION_HOME'], '/app/static/model/iris_knn.joblib']))
    #
    # target_names = ['setosa', 'versicolor', 'virginica']
    #
    # predictions = [{idx: target_names[value]} for idx, value in enumerate(knn.predict(new_data))]
    # if len(predictions) == 1:
    #     predictions = predictions[0]
    #
    # return jsonify(predictions)


# allow labeling of existing data
@bp.route('/model/label', methods=['POST'])
def label_existing_data():

    request_data = request.get_json()

    response = data.label_predictions(request_data)

    return response


# generate, store, and return model performance metrics
@bp.route('/model/eval', methods=['POST'])
def evaluate_model():
    request_data = request.get_json()

    request_data = data.extract_json_from_request(request_data)

    perf_col = data.get_mongo_collection(database='pocMLModelMonitoring', collection='irisKnnPerformance')

    # include option to get the most recently calculated model performance
    if request_data == 'latest':
        result = data.get_latest_perf_metrics(perf_col)
    # otherwise ensure correct args to get started
    elif not isinstance(request_data, dict) or 'mode' not in request_data.keys():
        return bad_request('POST data invalid, see model API')
    # then generate new model performance metrics based on supplied arguments
    else:
        pred_col = data.get_mongo_collection(database='pocMLModelMonitoring', collection='iris_knn')
        mode = request_data['mode']
        if mode == 'all':
            result = data.get_model_performance(pred_col)
        elif mode == 'dates':
            if 'start_date' not in request_data.keys() or 'end_date' not in request_data.keys():
                return bad_request('POST data invalid, see model API')
            else:
                result = data.get_model_performance(
                    pred_col,
                    mode='dates',
                    start_date=request_data['start_date'],
                    end_date=request_data['end_date']
                )
        elif mode == 'pct':
            if 'pct' not in request_data.keys():
                return bad_request('POST data invalid, see model API')
            else:
                result = data.get_model_performance(
                    pred_col,
                    mode='pct',
                    pct=request_data['pct']
                )
        elif mode == 'count':
            if 'count' not in request_data.keys():
                return bad_request('POST data invalid, see model API')
            else:
                result = data.get_model_performance(
                    pred_col,
                    mode='count',
                    pct=request_data['count']
                )
        else:
            return bad_request('POST data invalid, see model API')

        # write the new prediction to the model performance collection
        _ = perf_col.insert_one(result)

    if isinstance(result, dict) and '_id' in result.keys():
        del result['_id']

    # return the performance metrics
    return jsonify(result)
