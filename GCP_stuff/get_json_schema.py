def get_dict_schema(data):
    if isinstance(data, dict) and data != {}:
        keys = list(data.keys())
        result = [{key: get_dict_schema(data[key])} for key in keys]

        if len(result) == 1:
            result = result[0]

        return result

    elif data == {}:
        return 'empty dict'
    elif isinstance(data, list) and data != []:
        results = [get_dict_schema(item) for item in data]


        if isinstance(results, list) and all([isinstance(i, list) for i in results]):
                return results

        if any([i == 'str' for i in results]):
            return ['str']

        if any([i == 'float' for i in results]):
            return ['float']

        if not any([isinstance(i, dict) for i in results]) and len(set(results)) == 1:
            return [results[0]]

        return results

    elif data == []:
        return ['empty list']
    else:
        return type(data).__name__


def update_schema_file(schema1, schema2):
    if not isinstance(schema1, list) or not isinstance(schema2, list):
        if isinstance(schema1, dict):
            schema1 = [schema1]
        if isinstance(schema2, dict):
            schema2 = [schema2]
        if isinstance(schema1, str):
            if not isinstance(schema2, list):
                return f'error with schemas, you provided {type(schema1)} and {type(schema2)}'
        if isinstance(schema2, str):
            if not isinstance(schema1, list):
                return f'error with schemas, you provided {type(schema1)} and {type(schema2)}'


#     schema1 = sorted(schema1, key = lambda schema1: schema1['name'])
#     schema2 = sorted(schema2, key = lambda schema1: schema2['name'])

    result = [i for i in schema1 if i in schema2]

    only1 = [i for i in schema1 if i not in schema2]
    only2 = [i for i in schema2 if i not in schema1]

    if not only1 and not only2:
        return result

    n1 = [i.get('name') for i in only1]
    n2 = [i.get('name') for i in only2]

    unique = [i for i in n1 if i not in n2] + [i for i in n2 if i not in n1]

    result.extend([i for i in only1 if i.get('name') in unique])
    result.extend([i for i in only2 if i.get('name') in unique])

    similar = list(set(n1) & set(n2))

    if not similar:
        return result
    else:

        s1_versions = [i for i in schema1 if i.get('name') in similar]
        s2_versions = [i for i in schema2 if i.get('name') in similar]

        for name in similar:
            updated_version = {
                'name': name,
                'type': None,
                'mode': None
            }

            s1 = [i for i in s1_versions if i.get('name') == name][0]
            s2 = [i for i in s2_versions if i.get('name') == name][0]

            # added this, and moved everything over a level under the else clause
            if s1['type'] == 'empty' and s2['type'] != 'empty':
                updated_version = s2
            elif s2['type'] == 'empty' and s1['type'] != 'empty':
                updated_version = s1
            else:

                if 'fields' in s1.keys() and 'fields' in s2.keys():
                    # omg process field list

                    # check if fields are equal first
                    # must be able to handle the different field types (int, list, record)

                    updated_version['type'] = 'RECORD'

                    new_fields = update_schema_file(s1['fields'], s2['fields'])

                    updated_version['fields'] = new_fields

                # handle mode
                if s1['mode'] == s2['mode']:
                    updated_version['mode'] = s1['mode']
                else:
                    modes = [s1['mode'], s2['mode']]
                    if 'REPEATED' in modes:
                        new_mode = 'REPEATED'
                    elif 'REQUIRED' in modes:
                        new_mode = 'REQUIRED'
                    else:
                        new_mode = 'NULLABLE'
                    updated_version['mode'] = new_mode

                # different types
                if s1['type'] != s2['type']:
                    if 'fields' in s1.keys() or 'fields' in s2.keys():
                        updated_version['type'] = 'RECORD'
                    elif s1['type'] == 'STRING' or s2['type'] == 'STRING':
                        updated_version['type'] = 'STRING'
                    elif s1['type'] == 'FLOAT' or s2['type'] == 'FLOAT':
                        updated_version['type'] = 'FLOAT'
                else:
                    updated_version['type'] = s1['type']


            result.append(updated_version)

    return result


def convert_json_schema_to_bq(schema, mode='NULLABLE'):
    if isinstance(schema, dict):
        schema = [schema]
    if not isinstance(schema, list):
        return f'schema must be provided as a python dictionary or list. you provided {type(schema)}'

    mode = mode.upper()
    result = []

    def convert_type_string(s):
        if s == 'str':
            return 'STRING'
        elif s == 'int':
            return 'INTEGER'
        elif s == 'bool':
            return 'BOOLEAN'
        elif s == 'empty list':
            return 'empty'
        else:
            return 'FLOAT'

    for item in schema:
        if not isinstance(item, dict):
            return f'schema not formatted properly. double check that each item has a key: value pair.'

        (name, t), = item.items()

        if isinstance(t, dict):
            fields = convert_json_schema_to_bq(t, mode=mode)

            if isinstance(fields, dict):
                fields = [fields]

            entry = {
                'name': name,
                'type': 'RECORD',
                'mode': mode,
                'fields': fields
            }

        elif t in ['str', 'int', 'bool', 'float']:

            t = convert_type_string(t)

            entry = {
                'name': name,
                'type': t,
                'mode': mode
            }

        # moved this above the one below
        elif isinstance(t, list) and isinstance(t[0], list) and not all([i == t[0] for i in t]):
            sch = [convert_json_schema_to_bq(i, mode=mode) for i in t]
            fields = sch[0]

            if isinstance(fields, dict):
                fields = [fields]

            entry = {
                'name': name,
                'type': 'RECORD',
                'mode': 'REPEATED',
                'fields': fields
            }

        elif isinstance(t, list):
            if all([isinstance(i, str) for i in t]) and len(set(t)) == 1:
                t = convert_type_string(t[0])

                entry = {
                    'name': name,
                    'type': t,
                    'mode': 'REPEATED'
                }

            elif all([isinstance(i, dict) for i in t]) and len(set([list(i.keys())[0] for i in t])) != 1:

                fields = convert_json_schema_to_bq(t, mode=mode)

                if isinstance(fields, dict):
                    fields = [fields]

                entry = {
                    'name': name,
                    'type': 'RECORD',
                    'mode': 'NULLABLE',
                    'fields': fields
                }

            # new section start line 81
            elif all([isinstance(i, dict) for i in t]) and len(set([list(i.keys())[0] for i in t])) == 1:
                small_schema = []
                for field in t:
                    this_small_schema = convert_json_schema_to_bq(field, mode='NULLABLE')
                    small_schema = update_schema_file(small_schema, this_small_schema)

                small_schema = small_schema[0]

                small_schema['mode'] = 'REPEATED'

                entry = {
                    'name': name,
                    'type': 'RECORD',
                    'mode': mode,
                    'fields': small_schema
                }


            elif isinstance(t[0], list) and all([i == t[0] for i in t]):
                t = t[0]

                fields = convert_json_schema_to_bq(t, mode=mode)

                if isinstance(fields, dict):
                    fields = [fields]

                entry = {
                    'name': name,
                    'type': 'RECORD',
                    'mode': 'REPEATED',
                    'fields': fields
                }

        result.append(entry)

    return result


def make_bq_fields(fields):
    if isinstance(fields, dict):
        fields = [fields]
    if not isinstance(fields, list):
        return 'fields must be supplied as a list'

    def convert_data_type(t):
        if t == 'INTEGER':
            return 'INT64'
        elif t == 'FLOAT':
            return 'FLOAT64'
        elif t == 'BOOLEAN':
            return 'BOOL'
        else:
            return t

    result = ''

    for idx, field in enumerate(fields):
        if idx > 0:
            result += ', '

        t = convert_data_type(field.get('type'))

        if field.get('mode') == 'REPEATED':
            result += 'ARRAY<'

        name = field.get('name')

        if t == 'RECORD':
            fields2 = field.get('fields')
            result += f'{name} STRUCT<'
            res = make_bq_fields(fields2)

            result += f'{res}>'
        else:
            mode = field.get('mode')
            if mode == 'REPEATED':
                mode = 'NULLABLE'

            result += f'{name} {t} {mode}'

        if field.get('mode') == 'REPEATED':
            result += '>'

    return result


def make_bq_ddl(schema, project_id, dataset_id, table_name, replace=True):

    if not isinstance(schema, list):
        return 'schema must be provided as a list'

#     def convert_data_type(t):
#         if t == 'INTEGER':
#             return 'INT64'
#         elif t == 'FLOAT':
#             return 'FLOAT64'
#         elif t == 'BOOLEAN':
#             return 'BOOL'
#         elif t == 'RECORD':
#             return 'STRUCT'
#         else:
#             return t

    fields = make_bq_fields(schema)

    full_table_name = '.'.join([project_id, dataset_id, table_name])

    if replace:
        create = f'create or replace table `{full_table_name}`'
    else:
        create = f'create table if not exists `{full_table_name}`'

    create += f' ({fields})'

    return create


def generate_schema_for_file(file, gcs=True, schema=[]):
    """Opportunity to feed an existing schema into the function, which will be updated.
    Default is to start with an empty schema."""

    if gcs:
        blob = bucket.get_blob(file)
        text = blob.download_as_string()
        lines = text.decode('utf-8').split('\n')
    else:
        with open(file, 'r') as f:
            text = f.read()
        lines = text.split('\n')

    for idx, line in enumerate(lines):
        if line:
            line_data = json.loads(line)

            this_schema = get_dict_schema(line_data)
            bq_schema = convert_json_schema_to_bq(this_schema, mode='NULLABLE')
            schema = update_schema_file(schema, bq_schema)

    return schema


# usage
from google.cloud import storage
import json
import os
import tqdm

# gcs bucket location and path
gcs_bucket = 'bucket-id'
gcs_path = 'path/to/data'

project_id = 'project-id'

storage_client = storage.Client(project=project_id)

# double check these values
blobs = storage_client.list_blobs(gcs_bucket, prefix=gcs_path)

files = [
    blob.name for blob in blobs
    # if '.json' in blob.name  # only get certain file types
]

len(files)

bucket = storage_client.get_bucket(gcs_bucket)

# magic
schema = []

for file in tqdm.tqdm(files):
    # for file in files[:10]  # use only a subset of files
    schema = generate_schema_for_file(file, gcs=True, schema=schema)

# view final schema when done 

# generate ddl string to create the table with the schema detected
# this is bigquery format ddl
ddl = make_bq_ddl(schema, project_id, dataset_id, table_name, replace=True)
