"""
Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.

Created on 22 Apr 2018
@author: Richard Freeman

This Lambda queries DynamoDB for a specific partition and greater than a
specific sort key. This include X-ray decorators to create a full X-Ray Service map  

pip install aws-xray-sdk

"""
from __future__ import print_function
import logging
import boto3
import json
import decimal
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch

# from aws_xray_sdk.core import patch_all
patch(['boto3'])

from boto3 import resource
from boto3.dynamodb.conditions import Key


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HttpUtils:
    def __init__(self):
        pass

    @staticmethod
    def parse_parameters(event):
        try:
            return_parameters = event['queryStringParameters'].copy()
        except Exception:
            return_parameters = {}
        try:
            resource_id = event.get('path', '').split('/')[-1]
            if resource_id.isdigit():
                return_parameters['resource_id'] = resource_id
            else:
                return {"parsedParams": None, "err":
                    Exception("resource_id not a number")}
        except Exception as e:
            return {"parsedParams": None, "err": e}  # Generally bad idea to expose exceptions
        return {"parsedParams": return_parameters, "err": None}

    @staticmethod
    def respond(err=None, err_code=400, res=None):
        return {
            'statusCode': str(err_code) if err else '200',
            'body': '{"message":%s}' % json.dumps(err.message) if err else
            json.dumps(res, cls=DecimalEncoder),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }

    @staticmethod
    def parse_body(event):
        try:
            return {"body": json.loads(event['body']), "err": None}
        except Exception as e:
            return {"body": None, "err": e}


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class DynamoRepository:
    def __init__(self, table_name):
        self.dynamo_client = resource(service_name='dynamodb', region_name='eu-west-1')
        self.table_name = table_name
        self.db_table = self.dynamo_client.Table(table_name)

    @xray_recorder.capture('query')
    def query_by_partition_and_sort_key(self, partition_key, partition_value, sort_key, sort_value):
        xray_recorder.begin_subsegment('query')
        response = self.db_table.query(KeyConditionExpression=
                                       Key(partition_key).eq(partition_value)
                                       & Key(sort_key).gte(sort_value))
        xray_recorder.end_subsegment('query')
        return response.get('Items')

    @xray_recorder.capture('query')
    def query_by_partition_key(self, partition_key, partition_value):
        response = self.db_table.query(KeyConditionExpression=
                                       Key(partition_key).eq(partition_value))
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        xray_recorder.current_subsegment().put_annotation('get_response', status_code)
        return response.get('Items')

    @xray_recorder.capture('update')
    def update_dynamo_event_counter(self, event_name, event_datetime, event_count=1):
        response = self.db_table.update_item(
            Key={
                'EventId': event_name,
                'EventDay': event_datetime
            },
            ExpressionAttributeValues={":eventCount": event_count})
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        xray_recorder.current_subsegment().put_annotation('get_response', status_code)


def print_exception(e):
    print(''.join(['Exception ', str(type(e))]))
    print(''.join(['Exception ', str(e.__doc__)]))
    print(''.join(['Exception ', str(e.message)]))


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def get_dynamodb_records(event):
        try:
            validation_result = HttpUtils.parse_parameters(event)
            if validation_result.get('parsedParams', None) is None:
                return HttpUtils.respond(err=validation_result['err'], err_code=404)
            resource_id = str(validation_result['parsedParams']['resource_id'])
            if validation_result['parsedParams'].get("startDate") is None:
                result = repo.query_by_partition_key(partition_key="EventId", partition_value=resource_id)
            else:
                start_date = int(validation_result['parsedParams']['startDate'])
                result = repo.query_by_partition_and_sort_key(partition_key="EventId", partition_value=resource_id,
                                                              sort_key="EventDay", sort_value=start_date)
            return HttpUtils.respond(err=None, res=result)

        except Exception as e:
            print_exception(e)
            return HttpUtils.respond(err=Exception('Not found'), err_code=404)


table_name_global = 'user-visits-xray-sam'
repo = DynamoRepository(table_name=table_name_global)


def lambda_handler(event, context):
    response = Controller.get_dynamodb_records(event)
    return response
