"""
Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.

Created on 01 Apr 2018

@author: Richard Freeman
"""

from __future__ import print_function
import base64
import json
from boto3 import resource
from datetime import datetime
from collections import defaultdict
from time import time


class KinesisEvent:
    def __init__(self):
        self.event_name = ''
        self.page_id = ''
        self.action = 'skip'


class DynamoRepository:
    def __init__(self, target_dynamo_table, region='eu-west-1'):
        self.dynamo_db = resource(service_name='dynamodb', region_name=region)
        self.target_dynamo_table = target_dynamo_table
        self.expiration_time = int(time())  # TTL for DynamoDB generate once
        self.exception_counter = 0
        self.exception_counter_limit = 10

    def update_dynamo_event_counter(self, event_name, event_datetime, event_count=1):
        table = self.dynamo_db.Table(self.target_dynamo_table)
        table.update_item(
            Key={
                'EventId': str(event_name),
                'EventDay': event_datetime
            },
            ExpressionAttributeValues={":eventCount": event_count},
            UpdateExpression="ADD EventCount :eventCount")

    def add_defaultdict_to_dynamo(self, source_records, print_exception=False):
        for key, val in source_records.iteritems():
            try:
                self.update_dynamo_event_counter(key[0], key[1], int(val))
            except Exception as e:
                self.exception_counter += 1
                if self.exception_counter < self.exception_counter_limit:
                    print('Exception: DynamoDB update error')
                    Helper.print_exception(e)
                    print("Exception: %s, %s = %s" % (str(key[0]), str(key[1]), str(val)))


class Helper:
    def __init__(self):
        pass

    @staticmethod
    def extract_day_from_nano_timestamp(event_day):
        return int(datetime.fromtimestamp(event_day).strftime('%Y%m%d'))

    @staticmethod
    def print_exception(e):
        print(''.join(['Exception ', str(type(e))]))
        print(''.join(['Exception ', str(e.__doc__)]))
        print(''.join(['Exception ', str(e.message)]))


class KinesisRepository:
    def __init__(self):
        pass

    @staticmethod
    def parse_clickstream_event(payload_json, event_day, exception_counter, exception_counter_limit):

        try:
            kinesis_event = KinesisEvent()
            kinesis_event.event_day = event_day
            kinesis_event.event_name = payload_json.get('event_name', '')
            if kinesis_event.event_name in {'page view'}:
                kinesis_event.page_id = payload_json.get('page_id', '')
                if kinesis_event.page_id != '':
                    kinesis_event.action = 'count'
                else:
                    kinesis_event.action = 'skip'
            else:
                kinesis_event.action = 'skip'
            return kinesis_event

        except Exception as e:
            if exception_counter < exception_counter_limit:
                print('Exception: getting basic events %d/%d' %
                      (exception_counter, exception_counter_limit))
                print(''.join(['Exception: ', str(payload_json)]))
                Helper.print_exception(e)
                kinesis_event.action = 'exception'
            else:  # skip further exceptions
                kinesis_event.action = 'skip'
            return kinesis_event


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def count_kinesis_records_to_dynamo(event, context):

        processed_event_count = 0
        exception_counter = 0
        exception_counter_limit = 10
        event_name_day_counter = defaultdict(int)

        for record in event['Records']:
            try:
                approximate_arrival_timestamp = int(float(record['kinesis']['approximateArrivalTimestamp']))
                event_day = Helper.extract_day_from_nano_timestamp(approximate_arrival_timestamp)
                payload = base64.b64decode(record['kinesis']['data'])
                payload_json = json.loads(unicode(payload, errors='replace'))
                kinesis_event = KinesisRepository.parse_clickstream_event(payload_json, event_day, exception_counter,
                                                                          exception_counter_limit)
                if kinesis_event.action == 'skip':
                    continue
                elif kinesis_event.action == 'exception':
                    exception_counter += 1
                elif kinesis_event.action == 'count':
                    event_name_day_counter[(kinesis_event.page_id, kinesis_event.event_day)] += 1
                    processed_event_count += 1
                else:
                    exception_counter += 1
                    if exception_counter < exception_counter_limit:
                        print('Exception unexpected State')
                        if 'payload' in vars():
                            if len(payload) > 0:
                                print(''.join(['Exception: payload: ', str(payload)]))
                            else:
                                print('Exception: blank Kinesis payload')
                                print(''.join(['Exception: raw payload: ', str(record['kinesis'])]))
                        else:
                            print(''.join(['Exception: raw payload: ', str(record['kinesis']['data'])]))

            except Exception as e:
                exception_counter += 1
                if exception_counter < exception_counter_limit:
                    print('Exception: with event')
                    Helper.print_exception(e)
                    if 'payload' in vars():
                        if len(payload) > 0:
                            print(''.join(['Exception: payload: ', str(payload)]))
                        else:
                            print('Exception: blank Kinesis payload')
                            print(''.join(['Exception: raw payload: ', str(record['kinesis'])]))
                    else:
                        print(''.join(['Exception: raw payload: ', str(record['kinesis'])]))

        dynamoRepository.add_defaultdict_to_dynamo(event_name_day_counter, True)
        print('Counted: %s/%s' % (processed_event_count, len(event['Records'])))
        return


target_dynamo_table_global = 'user-visits-sam'
dynamoRepository = DynamoRepository(target_dynamo_table=target_dynamo_table_global)


def lambda_handler(event, context):
    Controller.count_kinesis_records_to_dynamo(event, context)
    return 'done'
