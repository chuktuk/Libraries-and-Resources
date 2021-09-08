#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains functions to make python ETL scripts easier to develop."""

# imports
import os
import pandas as pd
import jaydebeapi
import paramiko
from datetime import datetime as dt


# get data from obiee
def get_data_from_obiee(obiee_url, obiee_usr, obiee_pw, query, headers):
    """This function queries OBIEE and returns a basic dataframe.

    This dataframe will still need to be processed for data types or other data wrangling.

    It is recommended to use environment variables to parameterize the first three args.

    :param obiee_url: The URL to connect to OBIEE
    :param obiee_usr: The username to connect to OBIEE
    :param obiee_pw: The password associated with the OBIEE user
    :param query: The query string to send to OBIEE
    :param headers: The headers for the pandas dataframe
    :return: Returns a basic pandas dataframe
    """

    # set obiee connection params that never change
    java_driver_class = 'oracle.bi.jdbc.AnaJdbcDriver'
    jar = 'bijdbc.jar'

    # connect to obiee and submit the query
    with jaydebeapi.connect(jclassname=java_driver_class,
                            url=obiee_url,
                            driver_args={'user': obiee_usr,
                                         'password': obiee_pw},
                            jars=jar) as conn:
        with conn.cursor() as curs:
            curs.execute(query)
            dat = curs.fetchall()

    # create the dataframe
    df = pd.DataFrame(dat, columns=headers)
    df.drop(labels='s_0', axis='columns', inplace=True)

    return df


# get_ftp_client
# noinspection PyBroadException
def get_ftp_client(host, un, keyfilepath):
    """This function gets a paramiko ftp client for use with moving files.

    :param host: The host name to connect to.
    :param un: The username to use in the connection.
    :param keyfilepath: The path to the private key file for SSH connections.
    :return: Returns the ssh_client and ftp_client objects. These objects should be closed when finished.
    """

    # read in the key
    key = paramiko.RSAKey.from_private_key_file(keyfilepath)

    # return None if the connection fails
    try:
        # create the ssh_client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, username=un, pkey=key)

        # open an ftp client
        ftp_client = ssh_client.open_sftp()

        return ssh_client, ftp_client
    except Exception:
        return None, None


# upload_file_to_ftp
# noinspection PyBroadException,PyBroadException,PyBroadException,PyBroadException,PyBroadException,PyBroadException
def upload_files_to_ftp(files, ftp_client, app_home, mode='replace', age_days=14):
    """This function uploads one or more files to an ftp server.

    This function uses/assumes the following structure when uploading, moving, or deleting files:
    app_home/ contents include a dat folder and dat_old folder.

    File names must include the YYYYMMDD date as described in age_days for deletion of dat_old files.

    :param files: A single file or a list of files to upload, and should include the date as described in age_days.

    :param ftp_client: A paramiko ftp client object. The type of object returned by get_ftp_client() above.
                       This client object is NOT closed during this function.

    :param app_home: The full path to the directory where the app lives on the ftp server.
                     Example: D:/Apps/APP_NAME

    :param mode: The mode to use for replacing, updating, moving, and/or deleting files found on the file server.

                Available options:

                     'replace':  Moves all files in dat to dat_old (if a file already exists in dat_old, it is replaced
                                 with the file from dat).
                     'upsert':   Adds all uploaded files to dat, and moves any files that already exist there to
                                 dat_old. Does NOT move files to dat old that are not being replaced.
                     'abort':    Any files submitted to the function will not be added to the file server if the
                                 server contains a file with the exact same name as the file to upload. Any files
                                 not encountered will be uploaded if a list of files is passed. Existing files in dat
                                 are not moved to dat_old.

    :param age_days: The age of any files in dat_old to be removed. This requires that file names always follow
                     the format of file_name_YYYYMMDD.ext with the YYYYMMDD date located just before the .
                     Pass a very large number to not delete any files (10000000000000).
    """

    # ensure a list of files is present
    assert type(files) == str or type(files) == list

    if type(files) == str:
        files = [files]

    # change directory to app_home/dat
    dat_dir = ''.join([app_home, '/dat'])
    ftp_client.chdir(dat_dir)

    # get a list of the files in the dat dir
    dat_files = ftp_client.listdir()

    # change directory to app_home/dat_old
    dat_old_dir = ''.join([app_home, '/dat_old'])
    ftp_client.chdir(dat_old_dir)

    # get a list of dat_old files
    dat_old_files = ftp_client.listdir()

    # delete any dat_old files older than age_days
    for file in dat_old_files:
        end_char = file.find('.')
        start_char = end_char - 8
        file_date = file[start_char:end_char]
        if file_date.isnumeric():
            try:
                file_date = dt.strptime(file_date, '%Y%m%d')
                td = dt.now() - file_date
                # remove the dat_old file if too old or if replacing from dat
                if td.days > age_days or file in dat_files:
                    ftp_client.remove(file)
                    # if file is removed from dat_old, remove it from our list of dat_old_files
                    dat_old_files.remove(file)
            except Exception:
                pass
        elif file in dat_files:
            ftp_client.remove(file)
            dat_old_files.remove(file)

    # change back to the dat dir
    ftp_client.chdir(dat_dir)

    # get the current working directory
    curr_dir = os.getcwd().replace('\\', '/')

    # check the mode and iterate
    if mode == 'replace':
        # move all files in dat to dat_old
        for file in dat_files:
            try:
                # move the existing file from dat to dat_old
                ftp_client.rename(file, ''.join(['../dat_old/', file]))
            except Exception:
                pass
        for file in files:
            # upload the file to ftp dat folder
            try:
                # get the full path of the local file
                full_filename = '/'.join([curr_dir, file])
                # put the local file in the dat folder
                ftp_client.put(full_filename, file)
            except Exception:
                pass
    elif mode == 'upsert':
        # move files from dat to dat_old if being replaced
        for file in files:
            if file in dat_files:
                try:
                    # move existing file from dat to dat_old
                    ftp_client.rename(file, ''.join(['../dat_old/', file]))
                except Exception:
                    pass
            try:
                # get the full path of the local file
                full_filename = '/'.join([curr_dir, file])
                # put the local file in the dat folder
                ftp_client.put(full_filename, file)
            except Exception:
                pass
    else:  # elif mode == 'abort':
        for file in files:
            if file not in dat_files:
                try:
                    full_filename = '/'.join([curr_dir, file])
                    ftp_client.put(full_filename, file)
                except Exception:
                    pass

    return  # should probably keep track of results and return something
