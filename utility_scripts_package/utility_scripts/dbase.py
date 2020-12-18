#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""The dbase 'Database' module."""

import jaydebeapi
import os
import pandas as pd
from pymongo import MongoClient


def get_mongo_client(uri):
    """This function gets and returns a MongoClient object."""
    return MongoClient(uri)


def get_mongo_database(client, db):
    """Get and return a Mongo database using a MongoClient object."""
    return client[db]


def get_mongo_collection(db, collection):
    """Get and return a Mongo collection using a Mongo database object."""
    return db[collection]


def insert_into_mongo(data, collection):
    """Insert a python dictionary (one document) or a list of dictionaries (many documents) into a Mongo collection.

    :param data: a dictionary or list of dictionaries to insert into a mongo collection.
    :param collection: a mongo collection object.
    :return: returns a result object.
    """

    if type(data) == dict:
        result = collection.insert_one(data)
    elif type(data) == list:
        result = collection.insert_many(data)
    else:
        raise TypeError('data must be a dictionary or a list of dictionaries.')

    return result


def upsert_into_mongo(data, unique_id, collection):
    """This function will insert new records or update (by completely overwriting) existing records. This function
    will NOT update only the provided fields, and will fully overwrite any existing records with matching
    unique_id values.

    Records which have matching values specified by the key or list of keys supplied to unique_id.

    :param data: a dictionary or a list of dictionaries to insert or update in mongo db.
    :param unique_id: a string or list of strings representing the fields(s) or dictionary key names used as unique
                      identifiers for a record. Supplied values must match dictionary keys and mongo key/field names.
    :param collection: the mongo collection to insert and/or update records.
    :return: returns records_to_delete (list of the documents that were deleted (the old records)),
             delete_result (the delete result object), insert_result (the insert result object).
    """

    # ensure appropriate data type provided
    if type(data) == dict:
        data = [data]
    if type(data) != list or not all([type(i) == dict for i in data]):
        raise TypeError('data must be supplied as a dictionary or list of dictionaries.')
    if type(unique_id) == str:
        unique_id = [unique_id]

    # ensure unique_id is a list and all list items are strings
    if type(unique_id) != list or not all([type(i) == str for i in unique_id]):
        raise TypeError('unique_id must be supplied as a string or list of strings.')

    # check that the unique_id keys exist in each data record
    # add default value of None if it doesn't
    for i in data:
        for y in unique_id:
            if type(i) == dict and y not in i.keys():
                i[y] = None

    # create a list of dictionaries
    # each dictionary has all of the key/value pairs for each record
    data_combos = [{y: i[y] for y in unique_id} for i in data]

    # query the matching records from mongo and get all of the documents to be deleted
    deleted_records = [collection.find_one({y[0]: y[1] for y in i.items()}) for i in data_combos]
    # get a list of docs that are returned from the query, excluding None (null) results
    deleted_records = list(filter(None, deleted_records))
    # get the object ids from these records
    ob_ids_to_delete = [i['_id'] for i in deleted_records]

    # delete all records from mongo that were returned
    if ob_ids_to_delete:
        delete_result = collection.delete_many({'_id': {'$in': ob_ids_to_delete}})
    else:
        delete_result = 0

    # insert all data records into mongo, updating the deleted records
    insert_result = collection.insert_many(data)

    # return the results
    # deleted_records are the actual records from mongo that were deleted
    # delete_result is either 0 or the result object from delete_many
    # insert_result is the result object from insert_many
    return deleted_records, delete_result, insert_result


def close_mongo_client(client):
    """Close the connection to Mongo db."""
    client.close()


class OBIEEConnection:
    """OBIEE connection object.

    Attributes
    ----------
        java_driver_class:
            a string representing the java driver class

        url:
            the url to the OBIEE environment

        jar:
            the path to the .jar file used in the connection

        __driver_args:
            dictionary of strings supplying the 'user' and 'password'

    Methods
    -------
    submit_query:
        submits the supplied query to OBIEE and returns a pandas dataframe

    """

    def __init__(self, set_env=False, default_driver=True):
        if default_driver:
            self.java_driver_class = 'oracle.bi.jdbc.AnaJdbcDriver'
            self.jar = 'bijdbc.jar'
        else:
            self.java_driver_class = None
            self.jar = None
        if set_env:
            self.url = os.getenv('OBIEE_URL')
            self.__driver_args = {
                'user': os.getenv('OBIEE_USERNAME'),
                'password': os.getenv('OBIEE_PASSWORD')
            }
        else:
            self.url = None
            self.__driver_args = {
                'user': None,
                'password': None
            }

    @property
    def driver_args(self):
        return self.__driver_args

    @driver_args.setter
    def driver_args(self, value):
        check_types = all(
            [
                type(value) == dict,
                all([type(i) == str for i in list(value.values())])
            ]
        )
        if type(value) == dict and list(value) == ['user', 'password'] and check_types:
            self.__driver_args = value
        else:
            raise TypeError('driver_args must be a dictionary with string values for "user" and "password".')

    def submit_query(self, query):
        with jaydebeapi.connect(
                jclassname=self.java_driver_class,
                url=self.url,
                driver_args=self.__driver_args,
                jars=self.jar) as conn:
            with conn.cursor() as curs:
                curs.execute(query)
                dat = curs.fetchall()
                col_info = curs.description

        # get a list of columns
        columns = [i[0] for i in col_info]

        df = pd.DataFrame(dat, columns=columns)
        return df
