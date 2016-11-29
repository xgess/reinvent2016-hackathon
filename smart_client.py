import os
import csv
from io import StringIO
import json
from datetime import datetime
import random
from functools import partial

import requests


base_url = 'https://hackathon2.smartconservationtools.org:8443/server/api/query'
username = 'USERNAME'
password = 'PASSWORD'
auth_tuple = (username, password)

query_uuids = {
    'weapons': '2e7a7d85-1e83-4894-b996-1b55a68e7ba9',
    'weapons_seized': '139840bd-065f-4b54-8dca-ad79a5b02a69',
    'poacher_encounters': '74b42d17-dc3a-47c0-acb9-e9627cd3fa3c',
    'wildlife': '611a242e-4b38-4c5f-bab6-d292b55f2229',
    'people_observed': 'ab571879-0631-48b3-9ce4-e9ca0eacee44',
    'hunting_camp': 'd20a38f4-ed81-41c8-8569-864740a5ab26',
    'patrol_observation': '6f2c8df0-40d6-427c-9e1b-646fa85cee9a',
    'all_observations': '4912e088-547e-4f35-a695-2fdf7d490132'
}


def _retrieve_raw_data(endpoint, params={}):
    base_params = {
        'format': 'csv',
        'date_filter': 'waypointdate'
    }
    params.update(base_params)
    url = os.path.join(base_url, query_uuids[endpoint])
    response = requests.get(url, auth=auth_tuple, verify=False, params=params)
    return response.text


def process(text_response_data, operations):
    dict_reader = csv.DictReader(StringIO(text_response_data))

    list_of_dicts = []
    for dirty_dict in dict_reader:
        temp = dirty_dict
        for operation in operations:
            temp = operation(temp)        
        list_of_dicts.append(temp)
    return list_of_dicts


def operation_add_endpoint(endpoint, row):
    row['endpoint'] = endpoint
    return row

def operation_rename_latlong(row):
    row['longitude'] = row['X']
    row['latitude'] = row['Y']
    del row['X']
    del row['Y']
    return row

def operation_cleanup_timestamp(row):
    timestamp = row['Waypoint Date'] + ' ' + row['Waypoint Time']
    row['timestamp'] = datetime.strptime(timestamp, '%b %d, %Y %I:%M:%S %p').isoformat()
    del row['Waypoint Date']
    del row['Waypoint Time']
    return row

def operation_human_activity_filter(row):
    if row.get('Observation Category 0') == 'Human Activity':
        return row

def operation_remove_empty_values(row):
    compacted_row = { k: row[k] for k in row.keys() if row[k] != '' }
    return compacted_row

def _basic_operations(endpoint):
    cleaning_operations = [operation_rename_latlong, operation_cleanup_timestamp, operation_remove_empty_values]
    add_endpoint = partial(operation_add_endpoint, endpoint)
    return cleaning_operations + [add_endpoint]


def poaching_data(max_rows=200, categories=None, start_date=None, end_date=None):
    all_possible_endpoints = ['weapons', 'weapons_seized', 'poacher_encounters', 'wildlife', 'people_observed', 'hunting_camp', 'patrol_observation']
    if not categories:
        endpoints = all_possible_endpoints
    else:
        endpoints = [val for val in categories if val in all_possible_endpoints]
    
    params={}
    if start_date:
        params['start_date'] = _format_to_datestring(start_date)
    if end_date:
        params['end_date'] = _format_to_datestring(end_date)

    data_list = []
    for endpoint in endpoints:
        operation_functions = _basic_operations(endpoint)

        csv_data = _retrieve_raw_data(endpoint, params=params)
        clean_dicts = process(csv_data, operation_functions)
        data_list.extend(clean_dicts)
    
    truncated_data = data_list[0:max_rows]
    return {'data': truncated_data}


def human_activity_data(max_rows=200, start_date=None, end_date=None):
    endpoint = 'all_observations'
    operation_functions = _basic_operations(endpoint) + [operation_human_activity_filter]

    params={}
    if start_date:
        params['start_date'] = _format_to_datestring(start_date)
    if end_date:
        params['end_date'] = _format_to_datestring(end_date)


    csv_data = _retrieve_raw_data(endpoint, params=params)
    clean_dicts = process(csv_data, operation_functions)
    
    data_list = filter(lambda x: not not x, clean_dicts)

    truncated_data = data_list[0:max_rows]
    return {'data': truncated_data}


def _format_to_datestring(timestamp):
    return timestamp.strftime('%Y-%m-%d 00:00:00')

