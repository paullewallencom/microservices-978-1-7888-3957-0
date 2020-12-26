"""
Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.

Created on 01 Mar 2018
@author: Richard Freeman

This Lambda processes DynamoDB Streams records, 
and persists them into another DynamoDB.
There are no need to specify the source table as that is part of the event source, and
the target table is the same as the source with -replicated postfix. This means
that the lambda can be reused for the replication of similar tables without changes.

"""

from __future__ import print_function
from boto3 import resource


class DynamoRepository:
    def __init__(self):
        self.dynamodb = resource(service_name='dynamodb', region_name='eu-west-1')

    def update_dynamo_event_counter(self, table_name, full_parsed_row):
        table = self.dynamodb.Table(table_name)
        response = table.put_item(Item=full_parsed_row)
        print(response)


dynamoRepository = DynamoRepository()


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def parse_dynamo_type(item):
        datatype = item.keys()[0]
        if datatype == 'S':
            value = str(item.values()[0])
        elif datatype == 'N':
            value = int(item.values()[0])
        else:
            print('Datatype not supported yet!')
            value = None
        return value

    @staticmethod
    def replicate_dynamo_to_dynamo(event, context):
        processed_event_count = 0
        exception_counter = 0
        exception_counter_limit = 20
        target_table_name = ''
        for record in event['Records']:
            try:
                full_parsed_row = {}
                target_table_name = record['eventSourceARN'].split('/')[1] + '-replicated'

                for key, item in record['dynamodb']['NewImage'].iteritems():
                    value = Controller.parse_dynamo_type(item)
                    full_parsed_row[key] = value
                dynamoRepository.update_dynamo_event_counter(target_table_name, full_parsed_row)
                processed_event_count += 1
            except Exception as e:
                exception_counter += 1
                print('Exception DynamoDB update error')
                if exception_counter < exception_counter_limit:
                    print(''.join(['Exception ', str(record)]))
                    print_exception(e)
        # uncomment for large number of records
        print('Target Table %s %s/%s record(s)' % (target_table_name,
                                                   processed_event_count,
                                                   len(event['Records'])))


def print_exception(e):
    print(''.join(['Exception ', str(type(e))]))
    print(''.join(['Exception ', str(e.__doc__)]))
    print(''.join(['Exception ', str(e.message)]))


def lambda_handler(event, context):
    Controller.replicate_dynamo_to_dynamo(event, context)
    return 'done'
