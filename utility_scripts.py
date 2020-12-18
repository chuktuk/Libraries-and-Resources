#!/usr/bin/env python3
'''The utility_scripts module contains all purpose functions.

These functions are written for the purpose of a general or broad
application to various problems. Functions or classes stored here
are not specific to any one project.

Several of these functions contain dependencies on other python
modules. Check the docstrings with each function for more info.

Suggested module alias is 'us' for 'utility_scripts'.
'''

# import packages used in this module
import base64
import codecs
import fnmatch
import json
import logging
import paramiko
import pymongo
import pgpy
import re
import smtplib
import xmltodict

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime as dt
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm
from pgpy.constants import SymmetricKeyAlgorithm, CompressionAlgorithm
from pymongo import MongoClient



def get_xml_as_dict(file_path=None, data=None):
    '''This function accepts a file path to an xml doc or xml data and outputs a python dictionary.
    This is a generic function that should work with any xml file or data source.
    This function has dependencies on the xmltodict, json, re, and codecs packages.
    
    Arguments:
    file_path: default=None: the path and filename of the file to parse. Leave as None
    if using xml data already loaded as an object.
    
    data: default=None: the xml data to parse to a dictionary. Leave as None if getting
    data from a file.
    '''
    
    if file_path is None and data is None:
        print('No file path or data supplied: exiting function.')
        return
    
    # inner function to process encoding issues
    def unmangle_utf8(match):
        '''This is an inner function to deal with encoding errors in parsing json.
        '''
        escaped = match.group(0)                   # '\\u00e2\\u0082\\u00ac'
        hexstr = escaped.replace(r'\u00', '')      # 'e282ac'
        buffer = codecs.decode(hexstr, "hex")      # b'\xe2\x82\xac'

        try:
            return buffer.decode('utf8')           # '€'
        except: # UnicodeDecodeError:
            pass # print("Could not decode buffer: %s" % buffer)
    
    # parse the xml data to a dictionary string
    if file_path is not None:
        # read the data as a string
        with open(file_path) as xml_file:
            data = xmltodict.parse(xml_file.read())        
        # ensure the file is closed
        if xml_file.closed == False:
            xml_file.close()
    else:
        data = xmltodict.parse(data)
    
    # dump the data to json (still a string here)
    data = json.dumps(data)
    
    # replace 'null' with 'None' so python understands it
    data = data.replace('null', 'None')
    
    # fix encoding issues
    data = re.sub(r"(?i)(?:\\u00[0-9a-f]{2})+", unmangle_utf8, data).replace('\xa0', '')
    
    # evaluate the string as a python dictionary
    data = eval(data)
    
    # return the result
    return data

# create a file logger that can be used in multiple modules for an app
def create_file_logger(log_file, module_name, level='DEBUG'):
    '''This function creates a file logger to use for an app. 
    
    Dependencies:
    import logger
    
    This function should be called in every module within an app that logs events. 
    This function will create a file in the location specified by log_file. 
    Always supply __name__ for the module_name.
    
    Standard format for calling this function:
    logger = us.create_file_logger(log_file, __name__, level)
    
    Accepted values for level:
    'CRITICAL'
    'ERROR'
    'WARNING'
    'INFO'
    'DEBUG'
    
    Whichever level is supplied, every level above selection will also be logged.
    e.g. if level == 'WARNING' then 'WARNING', 'ERROR', and 'CRITICAL' are logged.
    
    
    Using the logger to log information about events with a custom message:
    logger.info('Message to log.')
    logger.info('%s a log message using %s', 'Writing', 'variables')
    
    Using the logger to report exceptions:
    try:
        statements that might fail
        logger.info('Success message.')
    except Exception as e:
        logger.exception(e)
        exception statements
    '''
    
    # create a logger
    logger = logging.getLogger(module_name)
    
    # create a filehandler
    fh = logging.FileHandler(log_file)
    
    # set the logger level and handler level
    if level == 'CRITICAL':
        logger.setLevel(logging.CRITICAL)
        fh.setLevel(logging.CRITICAL)
    elif level == 'ERROR':
        logger.setLevel(logging.ERROR)
        fh.setLevel(logging.ERROR)
    elif level == 'WARNING':
        logger.setLevel(logging.WARNING)
        fh.setLevel(logging.WARNING)
    elif level == 'INFO':
        logger.setLevel(logging.INFO)
        fh.setLevel(logging.INFO)
    elif level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)
    else:
        raise ValueError(''.join(['level must be one of the following: \'CRITICAL\', \'ERROR\', ',
                                 '\'WARNING\', \'INFO\', or \'DEBUG\'. ',
                                 'You entered ', '\'', level, '\'.']))
            #'''level must be one of the following: \'CRITICAL\', \'ERROR\', \'WARNING\', \'INFO\', or \'DEBUG\'. You entered '''level)
    
    # create a formatter and add to the file handler
    # this can be modified to produce different log entry formats
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    # add handler to the logger
    logger.addHandler(fh)
    
    # return the logger
    return logger

def process_log_for_errors(log_file, level='CRITICAL'):
    '''This function will process log files for errors. This function returns an email_log (boolean)
    based on whether 'level' or higher log entries are found, in addition to the highest level.
    
    Error hierarchy:
    CRITICAL > ERROR > WARNING > INFO > DEBUG
    
    Arguments:
    log_file: the path and filename of the log file to check for errors.
    
    level: default='CRITICAL': the level of error to check for. The error hierarchy is specified above.
    Supply this argument as a string.

    '''
    
    # read in the contents of the file
    with open(log_file, 'r') as file:
        contents = file.read()
    
    # ensure file is closed
    if file.closed == False:
        file.close()
    
    # check for the set level
    error_list = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    # check contents for any of the errors in error list, return True if any are found
    for error in error_list:
        if bool(re.search(error, contents)):
            highest_level = error
        # if after iterating, none have been found, return False and the 
    found_idx = error_list.index(highest_level)
    check_idx = error_list.index(level)
    
    if found_idx >= check_idx:
        return True, highest_level
    else:
        return False, highest_level
    

def shutdown_logging():
    '''Call this function to end logging once the app is completed.'''
    
    # get the root file logger
    logger = logging.getLogger()
    
    # shut it down
    logger.removeHandler('fh')
    
    # shutdown logging
    logging.shutdown()
    
def send_email(host, sender, recipient, subject, body, attachment=None, port=25):
    '''This function will send an email from the specified sender to
    the specified recipient, setting the subject and body as supplied.
    
    You can supply an optional attachment.
    
    Arguments:
        host: supply the email host as a string.
        
        sender: supply the email address of the sender as a string.
        
        recipient: supply the email address of the recipient as a string.
        
        subject: the subject of the email (string).
        
        body: the body content of the email (string).
        
        attachment: default=None: supply the full path to the attachment. Omit
        this argument if not sending an attachment.
        
        port: default=25: 25 is usually the port you want to use, but you may
        set it. Omit this arg if using the default port.'''
    
    # define the message
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # format and set teh attachment if present
    if attachment is not None:
        # set the filename
        if '\\' in attachment:
            attachment.replace('\\', '/')
        if '/' in attachment:
            idx = attachment.rfind('/') + 1
            filename = attachment[idx:]
        else:
            filename = attachment
            
        # read in the attachment
        with open(attachment, 'rb') as file:
            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload(file.read())
            encoders.encode_base64(payload)
            payload.add_header('Content-Disposition', 'attachment', filename=filename)
            message.attach(payload)
	
    with smtplib.SMTP(host, port) as smtp:
        #smtp.starttls()
        #smtp.login(sender, password)
        text = message.as_string()
        smtp.sendmail(sender, recipient, text)

def get_mongo_client(optional_URI=None):
    '''This function connects to mongo client and returns the MongoClient object.'''
    
    # set the URI key for working with mongoDB
    URI = 'mongodb://app:Mongodb123@mcmongodb01p:27017/test?authSource=admin&replicaSet=rs1&readPreference=primary&appname=MongoDB%20Compass&ssl=false'
    
    if optional_URI is None:
        return MongoClient(URI)
    else:
        try:
            return MongoClient(optional_URI)
        except Exception as e:
            print(type(e), e)

def get_mongo_database(client, db):
    '''Once the mongo client has been established, this function returns a database.
    You must supply the client object variable and the name of the database as a string.'''
    
    return client[db]

def get_mongo_collection(db, collection):
    '''Once a database object is created, this function returns a collection.
    You must supply the database object variable and the name of the collection as a string.'''
    
    return db[collection]

def insert_json_into_mongo(data, collection):
    '''This function accepts two arguments: a JSON-like data object (python dictionary or
    list of python dictionaries) and a collection object. For inserting many records,
    the data object should be a list of dictionaries, where each dicionary is a record.
    For inserting one record, a python dictionary should be passed or a list containing only
    one python dictionary.
    
    Returns a result object.'''
    
    if type(data) == dict:
        data = [data]
    
    if type(data) == list:
        result = collection.insert_many(data)
        
    return result

def upsert_into_mongo(data, unique_id, collection):
    '''This function is designed to "upsert" json like data into MongoDB. If a record
    already exists in the supplied mongo collection, it will be updated by completely
    overwriting the old record. If a record in the data does not exist in MongoDB,
    it will be added. 
    
    "upsert": verb. Update records that exist, insert records that don't exist.
    
    Arguments:
        data: a Python dictionary or a list of dictionaries, where each dictionary represents
        one record or document in MongoDB.
    
        unique_id: a string or a list of strings representing field(s) or dictionary key name(s) that serves as the 
        unique identifier(s) for each record. Supplied values must exist exactly in both 
        places (records in the data argument and records in the MongoDB collection).
    
        collection: a PyMongo collection object, representing the collection where data is
        to be upserted.
    
    returns:
        records_to_delete: the a list of records that were overwritten in the upsert statement.
        These are the full records. Empty list if no records were updated.
    
        insert_result: result object from `insert_many` for new records that were inserted.
        0 if no new records were inserted.
    
        delete_result: result object from `delete_many` on records that were updated in MongoDB.
        0 if no records were updated.
    '''
    
    # ensure appropriate data type provided
    if type(data) == dict:
        data = [data]
    
    # ensure unique_id is treated as a list 
    if type(unique_id) == str:
        unique_id = [unique_id]
        
    assert type(data) == list, 'A dictionary or list must be passed for "data".'
    #assert type(unique_id) == str, 'A string must be passed for "unique_id".'
    
    # ensure unique_id is a list and all list items are strings
    assert type(unique_id) == list, 'A string or list of strings must be passed for "unique_id".'
    for i in unique_id:
        assert type(i) == str, 'A string or list of strings must be passed for "unique_id".'

    # check that the unique_id keys exist in each data record
    # add default value of None if it doesn't
    for i in data:
        for y in unique_id:
            if type(i) == dict and y not in i.keys():
                i[y] = None

    # create a list of dictionaries
    # each dictionary has all of the key/value pairs for each record
    data_combos = [{y: i[y] for y in unique_id} for i in data]
    
    # create an empty list to append query results
    records_to_delete = []
    # iterate through the data_combos, unique ids and values in the data
    for i in data_combos:
        # search for records in mongo that contain the combination in the new data
        records_to_delete.append(collection.find_one({y[0]: y[1] for y in i.items()}))
    # get a list of docs that are returned from the query
    records_to_delete = [i for i in records_to_delete if i is not None]
    # get the object ids from these records
    ob_ids_to_delete = [i['_id'] for i in records_to_delete]
    
    # delete all records from mongo that were returned
    if ob_ids_to_delete != []:
        delete_result = collection.delete_many({'_id': {'$in': ob_ids_to_delete}})
    else:
        delete_result = 0
    
    # insert all data records into mongo, updating the deleted records
    insert_result = collection.insert_many(data)
    
    # return the results
    # records_to_delete are the actual records from mongo that were deleted
    # delete_result is either 0 or the result object from delete_many
    # insert_result is the result object from insert_many
    return records_to_delete, delete_result, insert_result

def close_mongo_client(client):
    '''This function closes the mongo client connection and frees those resources.'''
    
    # close connection
    client.close()
    
def get_sftp_client(host, username, password, port=22, keyfilepath=None, keyfiletype=None):
    '''This function returns an active sftp client connection and an active transport object. 
    This connection must be closed when finished using transport.close() and client.close().
    
    Arguments:
    host: the domain for the host to which a connection will be made.
    
    username: the username for the connection.
    
    password: the password for the connection.
    
    port: default=22: the port to use to make the sftp connection.
    
    keyfilepath: default=None: if using a private key file to connect to the sftp site.
    
    keyfiletype: default=None: either 'DSA' or 'RSA' for key type.
    '''
    
    # initialize variables
    sftp = None
    key = None
    transport = None
    
    # create connection
    try:
        # check for a keyfile
        if keyfilepath is not None:
            if keyfiletype == 'DSA':
                key = paramiko.DSSKey.from_private_key_file(keyfilepath)
            else:
                key = paramiko.RSAKey.from_private_key_file(keyfilepath)
        
        # initiate a transport object and connect to it
        transport = paramiko.Transport((host, port))
        transport.connect(None, username, password, key)
        
        # get the sftp client from transport
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # return the sftp client
        return transport, sftp
    
    except Exception as e:
        print(f'An error occurred creating SFTP client: {type(e)}: {e}')
        # ensure connections are closed if there is an issue connection
        if sftp is not None:
            sftp.close()
        if transport is not None:
            transport.close()
        pass
    
def get_key_from_file(path_to_key_file):
    '''This function gets a key from a file. This function will return a private
    key or a public key depending on the contents of the file. Private keys cannot
    decrypt data without having the password to unlock them.
    
    Supply the path_to_key_file as a string. Key files are typcially .asc files.'''
    
    # load the key from file
    key, _ = pgpy.PGPKey.from_file(path_to_key_file)
    
    return key

def create_private_key(username, comment, email, password, new_key_file):
    '''This function uses the pgpy module to create a basic private key with its
    own public key that can be used for encrypting/decrypting messages.
    
    Arguments:
    username: the primary username for this key.
    
    comment: a comment required for creating the user. Can simply be a description of the user.
    
    email: the email address for the user
    
    password: the password you are choosing to lock/protect the private key. This
    password will not be accessible once created, so be sure you remember it.
    
    new_key_filename: the path and filename for the new key file. Will throw an exception
    if the file already exists. Use extension .asc for the new_key_filename.
    '''
    
    # create a new key object
    key = pgpy.PGPKey.new(key_algorithm=PubKeyAlgorithm.RSAEncryptOrSign, key_size=4096)
    
    # create a user ID for the key
    uid = pgpy.PGPUID.new(pn=username, comment=comment, email=email)
    
    # add the userid to the key and set key usage
    key.add_uid(uid=uid, usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
                hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA384, HashAlgorithm.SHA512, HashAlgorithm.SHA224],
                ciphers=[SymmetricKeyAlgorithm.AES256, SymmetricKeyAlgorithm.AES192, SymmetricKeyAlgorithm.AES128],
                compression=[CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2, CompressionAlgorithm.ZIP,
                             CompressionAlgorithm.Uncompressed])
    
    # set the password for the private key
    key.protect(password, SymmetricKeyAlgorithm.AES256, HashAlgorithm.SHA256)
    
    # ensure the key is password protected
    assert key.is_protected == True, 'Key generation of unprotected private keys is not allowed.'
    
    # store the private key in the specified file
    with open(new_key_file, 'x') as file:
        file.write(str(key))
        
def decrypt_file(source_file, pvtkey, password, mode='return', dest_file=None, rmv_extra_returns=True):
    '''This function will decrypt an encrypted file, provided the correct private key (pvtkey)
    is supplied with the correct password. The decrypted data can be either written to a file or
    returned as an object (see Arguments).
    
    Arguments:
    source_file: the path and name of the file to decrypt. Should be a .txt file.
    
    pvtkey: the private key object associated with the file to decrypt. Could also be the
    path to a private key.
    
    password: the password for the locked private key.
    
    mode: default='return':the decrypted data will be returned as an object. 
    The type of object returned may vary depending on the contents of the file. 
    mode='file': the decrypted data will be written to a file. The dest_file 
    argument must also be supplied when using 'file'.
    
    dest_file: default=None: the path and name of the output file containing the decrypted data.
    Will throws an exception if this file already exists. If writing to a file, the 'mode' must
    be set to 'file'.
    
    rmv_extra_returns: default=True: experiments with this package indicate that some
    line endings may be altered during conversions. This setting will remove \r type 
    returns from the message before writing to a file.
    
     
    '''
    
    # check inputs for validity
    if mode == 'file':
        assert dest_file is not None, 'If using mode="file", dest_file must be supplied.'
    else:
        assert mode == 'return', 'mode must be either "file" or "return".'
    
    # read in the message from an encrypted file
    message_from_file = pgpy.PGPMessage.from_file(source_file)
    
    if type(pvtkey) == pgpy.pgp.PGPKey:
        # decrypt the message
        with pvtkey.unlock(password):
            # get the decrypted message
            decrypted_message = pvtkey.decrypt(message_from_file)
    elif type(pvtkey) == str:
        key, _ = pgpy.PGPKey.from_file(pvtkey)
        with key.unlock(password):
            # get the decrypted message
            decrypted_message = key.decrypt(message_from_file)
        
    # ensure message is decrypted
    assert decrypted_message.is_encrypted == False
        
    # decode the message
    if type(decrypted_message.message) == str:
        contents = decrypted_message.message
    else:
        contents = decrypted_message.message.decode()
        
    # remove extra hard returns that were added
    if rmv_extra_returns:
        contents = contents.replace('\r', '')
        
    # delivery of decrypted data
    if mode == 'file':
        # write the decrypted file
        with open(dest_file, 'x') as output_file:
            output_file.write(contents)
    else:
        return contents
        
def create_public_key_file(private_key, public_key_file):
    '''This function will create a public key file paired with the private key supplied.
    The public key can be used to encrypt files, but cannot be used to decrypt them.
    
    Arguments:
    private_key: either the private key object or the path to a private key.
    
    public_key_file: the file path and name for the new public key file to generate. Use the file 
    extension .asc when supplying this filename. Throws an exception if the file already exists.
    '''
    
    if type(private_key) == pgpy.pgp.PGPKey:
        # get the public key
        pub_key = private_key.pubkey
    elif type(private_key) == str:
        key, _ = pgpy.PGPKey.from_file(private_key)
        pub_key = key.pubkey
    
    # write the public key file
    with open(public_key_file, 'x') as file:
        file.write(str(pub_key))
        
def encrypt_file(source_file, dest_file, public_key):
    '''This function creates a new encrypted file from a source file
    and a public key.
    
    Arguments:
    source_file: the path and filename of the source file to be encrypted. Source
    file does not have to be a particular format.
    
    dest_file: the path and filename of the destination file. Use file extension
    .txt for the destination file. Throws and exception if the file already exists.
    
    public_key: the public key object or filename of the public key.
    '''
    
    # access the public key if a string is passed for the public_key
    if type(public_key) == str:
        public_key, _ = pgpy.PGPKey.from_file(public_key)
    
    # generate a message from the file contents
    message = pgpy.PGPMessage.new(source_file, file=True)
    
    # encrypt the message
    encrypted_message = public_key.encrypt(message)
    
    # ensure message is encrypted before writing to file
    assert encrypted_message.is_encrypted == True
    
    # write the encrypted file
    with open(dest_file, 'x') as output_file:
        output_file.write(str(encrypted_message))