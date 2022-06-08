#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""Process files for MFT exports. Reads all files in a GCS bucket and combines them
into files of a set maximum size for MFT exports."""


# standard library imports
import os
from datetime import datetime as dt

# custom module imports
import log
import utils


# main function to call when the app is executed
if __name__ == '__main__':
    
    # parse cli args
    args = utils.parse_args()
    disable_logging = args.disable_logging
    input_dir = args.input_dir
    output_dir = args.output_dir
    extension = args.extension
    split_prefix = args.write_prefix
    max_size = args.max_file_size
    disable_gzip = args.disable_gzip
    
    # validate arguments
    _ = utils.validate_dir_formats(input_dir)
    _ = utils.validate_dir_formats(output_dir)
    
    # raise an exception if output_dir exists and isn't empty
    _ = utils.validate_output_dir(output_dir)

    # get username for log and output dir
    user = os.getenv('JUPYTERHUB_USER', 'nousername')
    
    # initate logging
    if disable_logging:
        # create dummy vars if logging disabled
        log_message = 'Logging disabled. Good luck troubleshooting without logs.'
        print(log_message)
        logger = log.EmptyLogger()
    else:
        # extract date for log file name
        file_date = dt.now().strftime('%Y%m%d_%f')
        log_file = f'{user}_{file_date}_mft_export_log.log'
        
        log_message = f'Check the log file {log_file} for details.'
        
        # create the logger
        logger = utils.create_logger(log_file)
            
    # add date and userid to output path
    output_path = f'{output_dir}/{dt.now().strftime("%Y%m%d")}/{user}'
    
    # get the data and log paths
    output_data_dir = f'{output_path}/data'
    output_log_dir = f'{output_path}/log'
        
    # FILE PROCESSING
        
    # process json files
    if extension == 'json':
        
        # get a dask dataframe
        try:
            ddf = ddf = utils.get_dask_df(input_dir)
            message = 'Input data read successfully. Processing files.'
            print(message)
            logger.info(message)
            print(f'Output location: {output_path}')
        except Exception as e:
            error_message = f'Error getting dask dataframe from {input_dir}. Operation aborted. See log for details.'
            print(error_message)
            utils.exit_on_error(logger, e, error_message, log_message)
    
        # write the dask dataframe to json files in chunks
        total_lines, outfiles = utils.write_dask_df_to_json(
            ddf, 
            split_prefix,
            output_data_dir,
            max_size, 
            disable_gzip,
            logger, 
            log_message
        )
    
    # process csv files
    elif extension == 'csv':
        try:
            ddf = utils.get_dask_df(input_dir)
            message = 'Input data read successfully. Processing files.'
            print(message)
            logger.info(message)
            print(f'Output location: {output_path}')
        except Exception as e:
            error_message = f'Error getting dask dataframe from {input_dir}. Operation aborted. See log for details.'
            print(error_message)
            utils.exit_on_error(logger, e, error_message, log_message)
        
        total_lines, outfiles = utils.write_dask_df_to_csv(
            ddf, 
            split_prefix, 
            output_data_dir,
            max_size, 
            disable_gzip,
            logger, 
            log_message
        )
        
    else:
        raise ValueError('extension must be json or csv')
    
    # format total lines count with commas
    total_lines = '{:,}'.format(total_lines)
    
    # log total lines written
    success_message = f'Data processing completed. {total_lines} total lines were processed.'
    logger.info(success_message)
            
    # end logging and transfer the log file
    utils.destroy_logger(logger)
    
    # move log to the output dir
    if not disable_logging:
        try:
            # write the log file to gcs
            _ = utils.gsutil_output_files_to_gcs(output_log_dir, log_file, disable_gzip=True)
            print(f'Log file location {output_log_dir}/{log_file}.')
        except Exception as e:
            print(f'Error moving log to GCS. Log file is available locally at {log_file}.')
    
    # print success
    print(f'Script completed successfully. {total_lines} rows processed.')
    print(success_message)
    