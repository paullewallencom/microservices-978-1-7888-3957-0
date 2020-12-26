"""
Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.


Created on 09 Apr 2018
@author: Richard Freeman

This Lambda read messages off a queue

"""

from __future__ import print_function
import logging
import boto3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SqsRepository:
    def __init__(self, queue_name):
        self.sqs_resource = boto3.resource('sqs', region_name='eu-west-1')
        self.queue_name = queue_name
        self.sqs_queue = self.sqs_resource.get_queue_by_name(QueueName=self.queue_name)
        self.sqs_client = boto3.client(service_name='sqs', region_name='eu-west-1')

    def send_message(self, json_body):
        try:
            response = self.sqs_queue.send_message(MessageBody=json_body)
            return response
        except Exception as e:
            print_exception(e)
            return e

    def delete_message(self, receipt_handle):
        """
        Uses the receipt_handle to delete a message.
        
        Note For FIFO SQS the receipt_handle has a limited lifespan
        """
        try:
            response = self.sqs_client.delete_message(QueueUrl=self.sqs_queue.url,
                                                      ReceiptHandle=receipt_handle)
            return response
        except Exception as e:
            print_exception(e)


def print_exception(e):
    logger.error(''.join(['Exception ', str(type(e))]))
    logger.error(''.join(['Exception ', str(e.__doc__)]))
    logger.error(''.join(['Exception ', str(e.message)]))


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def process_sqs_messages(event, max_iterations=5,
                             max_message_batch=1,
                             waittime_between_messages=1,
                             message_visibility=5):

        # TODO when SQS Lambda event source is available use event data.
        # For now can query SQS directly for up to max_mesages
        # As Lambdas have a max TTL of 5min
        processed_counter = 0
        for i in range(0, max_iterations):  # up to 20 messages
            response_messages = sqsRepo.sqs_client.receive_message(
                QueueUrl=sqsRepo.sqs_queue.url,
                MaxNumberOfMessages=max_message_batch,
                VisibilityTimeout=message_visibility,
                WaitTimeSeconds=waittime_between_messages)
            if response_messages.get('Messages') is not None:
                for message in response_messages['Messages']:
                    try:
                        print(message['Body'])
                        # TODO Process message body here
                        delete_response = sqsRepo.delete_message(message['ReceiptHandle'])
                        logger.info(delete_response)
                        processed_counter += 1
                    except Exception as e:
                        logger.error('print_exception(%s)' % str(e))

        return '%d messages processed' % processed_counter


queue_name_global = 'user-visits-sam.fifo'
sqsRepo = SqsRepository(queue_name=queue_name_global)


def lambda_handler(event, context):
    response = Controller.process_sqs_messages(event=event)
    return response
