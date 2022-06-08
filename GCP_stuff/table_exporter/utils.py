#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""Utility functions for the export_mft app. Contains functional code for the app."""


import os
import re
import sys
import tqdm
import shlex
import argparse
import logging
import subprocess
import dask.dataframe as dd

# custom imports
import log


# parse args
def parse_args():
        
    # app description
    desc = '''MFT Export App. Input data must be parquet. Will output gzipped files in either csv or json format.
    '''
    
    # check for logging argument
    parser = argparse.ArgumentParser(
        prog='mft_export',
        description=desc,
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=36)
    )
    
    parser.add_argument(
        '--extension',
        choices={'csv', 'json'},
        help='REQUIRED. Extension for the output files. These will be gzipped.',
        required=True
    )
    
    parser.add_argument(
        '--input_dir',
        help='REQUIRED. The GCS location for the parquet input files. Required format: gs://bucket_id/path/to/files',
        required=True
    )
    
    parser.add_argument(
        '--output_dir',
        help='REQUIRED. The GCS location for the output files. Required format: gs://bucket_id/path',
        required=True
    )
            
    parser.add_argument(
        '--max_file_size',
        default=10,
        type=int,
        help='Maximum file size to create in GB before gzipping. (Default: 10)'
    )
        
    parser.add_argument(
        '--disable_logging', 
        default=False,
        action='store_true',
        help='Turn on this flag to disable logging. (Default: False)'
    )
    
    parser.add_argument(
        '--disable_gzip', 
        default=False,
        action='store_true',
        help='Turn on this flag to disable gzip feature. (Default: False)'
    )
    
    parser.add_argument(
        '--write_prefix',
        default='DATA',
        help='The prefix to use for filenames. File names will be incremented. (Default: DATA)'
    )
    
    args = parser.parse_args()
    
    return args


# exit app due to error
def exit_on_error(logger, e, error_message, log_message):
    """Log error message, shutdown logging, and exit the app."""
        
    logger.critical(error_message)
    logger.critical(f'{type(e)}: {e}')
    logger.critical(f'Exiting script.')
    destroy_logger(logger)
    logging.shutdown()
    
    sys.exit(f'{error_message} {log_message}')


# validate the input and output dir formats
def validate_dir_formats(value):
    """Validate that the input_dir and output_dir are supplied as gs://<bucket_id>/<path>."""
    
    pattern = re.compile('gs://\S+/\S+')
    
    if isinstance(value, list) and all([isinstance(i, str) for i in value]):
        result = all([pattern.match(d) for d in value])
    elif isinstance(value, str):
        result = pattern.match(value)
    else:
        raise TypeError(f'Invalid type passed to validate_dir_format. You supplied {type(value)}. Str or list of strings required.')
        
    if not result:
        raise ValueError(f'GCS dir values must be formatted gs://bucket_id/path.')
            
    return True


# ensure the output_dir either doesn't exist or is empty
def validate_output_dir(output_dir):
    """Throw an exception if the output_dir exists and isn't empty."""

    command = f'gsutil ls {output_dir}'

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, _ = process.communicate()
    output_dir_objects = output.decode().split('\n')

    if output_dir_objects != [''] and output_dir_objects != [f'{output_dir}/', '']:
        raise FileExistsError(f'{output_dir} already exists and is not empty. Specify a different output_dir or delete contents before running.')

    return True


# initiate logging function
def create_logger(log_file, level='DEBUG'):
    """Create logger and start logging. To disable logging, call the app with --logging=False flag."""
    
    # initiate logging
    logger = log.create_file_logger(log_file, __name__, level=level)
    
    # log start
    logger.info(f'------------------ BEGIN MFT EXPORT PROCESSING ------------------')
    
    return logger


# end logging
def destroy_logger(logger):
    """End logging and cleanup the logger."""
    
    logger.info(f'------------------- END MFT EXPORT PROCESSING -------------------')
    fh = logger.handlers[0]
    logger.removeHandler(fh)
    
    logging.shutdown()
    
    return


# get dask dataframe from parquet files (very quick)
def get_dask_df(input_uri):
    """Gets a dask dataframe from parquet files."""
    
    uri = input_uri.replace('.parquet', '')
    
    # must use pyarrow engine to preserve json structure in fields
    ddf = dd.read_parquet(f'{uri}.parquet', engine='pyarrow')
    
    return ddf


# write dask dataframe to csv in chunks
def write_dask_df_to_csv(
    ddf, 
    split_prefix, 
    output_data_dir,
    max_size, 
    disable_gzip,
    logger, 
    log_message
):
    
    # create the first filename
    i = 0
    file_num_str = f'{i}'.zfill(8)
    extension = 'csv'
    this_outfile = f'{split_prefix}{file_num_str}.{extension}'

    # remove any stale versions of this_outfile if they exist
    if os.path.exists(this_outfile):
        os.remove(this_outfile)

    # convert max_size from GB to bytes
    size = max_size * 1_000_000_000

    # add it to the list of filenames
    outfiles = [this_outfile]

    # initiate a total line counter
    total_lines = 0

    # get the number of dask partitions to add a progress bar
    num_partitions = ddf.npartitions

    # create a progress bar
    pbar = tqdm.tqdm(desc='Writing data partitions to csv', total = num_partitions)

    # set first run
    first = True

    for p in ddf.partitions:
        # ensure we get the header for the first file
        if first:
            header = True
            first = False
        # if the file isn't full don't append a header to an existing csv
        elif os.path.getsize(this_outfile) < size:
            header = False
        else:
            # move the full file to gcs first
            try:
                _ = gsutil_output_files_to_gcs(output_data_dir, this_outfile, disable_gzip)
                logger.info(f'{this_outfile} successfully moved to {output_data_dir}')
            except Exception as e:
                error_message = f'Error moving {this_outfile} to GCS'
                print(f'{error_message}. See log for details.')
                logger.error(error_message)
                logger.error(f'{type(e)}: {e}')
            
            # increment and create a new file
            i += 1
            file_num_str = f'{i}'.zfill(8)
            this_outfile = f'{split_prefix}{file_num_str}.{extension}'
            # remove any stale versions of this_outfile if they exist
            if os.path.exists(this_outfile):
                os.remove(this_outfile)

            # set header true for a new file
            header = True
            outfiles.append(this_outfile)

        try:
            df = p.compute()
            total_lines += df.shape[0]
            df.to_csv(this_outfile, sep='|', mode='a', header=header, index=False)
        except Exception as e:
            error_message = f'Critical error processing dask dataframe partition. Export unsuccessful. See log for details.'
            print(error_message)
            exit_on_error(logger, e, error_message, log_message)

        # update the progress bar after each partition
        pbar.update(1)
        
    # move final outfile to gcs
    try:
        _ = gsutil_output_files_to_gcs(output_data_dir, this_outfile, disable_gzip)
        logger.info(f'{this_outfile} successfully moved to {output_data_dir}')
    except Exception as e:
        error_message = f'Error moving {this_outfile} to GCS'
        print(f'{error_message}. See log for details.')
        logger.error(error_message)
        logger.error(f'{type(e)}: {e}')
    
    return total_lines, outfiles


# write dask df to newline json
def write_dask_df_to_json(
    ddf, 
    split_prefix,
    output_data_dir,
    max_size, 
    disable_gzip,
    logger, 
    log_message
):
        
    # create the first file
    i = 0
    file_num_str = f'{i}'.zfill(8)
    extension = 'json'
    this_outfile = f'{split_prefix}{file_num_str}.{extension}'

    # remove any stale versions of this_outfile if they exist
    if os.path.exists(this_outfile):
        os.remove(this_outfile)

    # convert max_size from GB to bytes
    size = max_size * 1_000_000_000

    # add it to the list of filenames
    outfiles = [this_outfile]

    # initiate a total line counter
    total_lines = 0

    # get the number of partitions in the dask dataframe
    num_partitions = ddf.npartitions
    
    # initialize the first file -> don't gzip until after the file is done
    with open(this_outfile, 'w'):
        pass

    # create a progress bar
    pbar = tqdm.tqdm(desc='Writing data partitions to json', total = num_partitions)

    for p in ddf.partitions:
        # if this_outfile isn't full, keep going
        if os.path.getsize(this_outfile) < size:
            pass
        else:
            # otherwise move the full file to gcs first
            try:
                _ = gsutil_output_files_to_gcs(output_data_dir, this_outfile, disable_gzip)
                logger.info(f'{this_outfile} successfully moved to {output_data_dir}')
            except Exception as e:
                error_message = f'Error moving {this_outfile} to GCS'
                print(f'{error_message}. See log for details.')
                logger.error(error_message)
                logger.error(f'{type(e)}: {e}')

            # increment and create a new file
            i += 1
            file_num_str = f'{i}'.zfill(8)
            this_outfile = f'{split_prefix}{file_num_str}.{extension}'
            # remove any stale versions of this_outfile if they exist
            if os.path.exists(this_outfile):
                os.remove(this_outfile)
            outfiles.append(this_outfile)

        # process this partition
        try:
            df = p.compute()
            total_lines += df.shape[0]
            with open(this_outfile, 'a') as f:
                df.to_json(f, orient='records', lines=True)
        except Exception as e:
            error_message = f'Critical error processing dask dataframe partition. Export unsuccessful. See log for details.'
            print(error_message)
            exit_on_error(logger, e, error_message, log_message)

        # update the progress bar after each partition
        pbar.update(1)
        
    # move final outfile to gcs
    try:
        _ = gsutil_output_files_to_gcs(output_data_dir, this_outfile, disable_gzip)
        logger.info(f'{this_outfile} successfully moved to {output_data_dir}')
    except Exception as e:
        error_message = f'Error moving {this_outfile} to GCS'
        print(f'{error_message}. See log for details.')
        logger.error(error_message)
        logger.error(f'{type(e)}: {e}')
    
    return total_lines, outfiles


# copy outfiles to gcs using gsutil -> much faster and can gzip while moving
def gsutil_output_files_to_gcs(output_dir, file, disable_gzip=False):
    """Calls gsutil_cp.sh shell script to upload and gzip an outfile"""
                    
    if disable_gzip:
        command = f'./gsutil_cp.sh {file} {output_dir}'
    else:
        command = f'./gsutil_gzip_cp.sh {file} {output_dir}'
    _ = subprocess.call(shlex.split(command))
    
    return True
