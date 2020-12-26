"""
Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.


Created on 14 Apr 2018

@author: Richard Freeman

This package sends records to SQS

"""

import logging
import json

import boto3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def write_message_fifo(queue_name, json_body,
                       sqs_resource=boto3.resource('sqs', region_name='eu-west-1')):
    try:
        queue = sqs_resource.get_queue_by_name(QueueName=queue_name)
        response = queue.send_message(MessageBody=json_body, MessageGroupId='sample-message')
        return response
    except Exception as e:
        logger.error(str(type(e)))
        logger.error(str(e.__doc__))
        logger.error(str(e.message))
        return None


def send_sample_message(queue_name):
    """
    This sends a sample message to a FIFO Queue
    
    Note with content deduplication enabled identical messages will
    get a 200 response code but it will not be added to the queue!
    """

    d = {}
    d['user_id'] = 'SD23hj35'
    d[
        'user_agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36."
    d['referer'] = "https://www.google.com/"
    d['url'] = "https://www.mysite.com/timeline"
    d['event_name'] = "page view"
    d['page_id'] = "1254"
    json_body = json.dumps(d)
    return write_message_fifo(queue_name=queue_name,
                              json_body=json_body)


def main():
    queue_name = 'user-visits-sam.fifo'
    response = send_sample_message(queue_name=queue_name)
    logger.info(response)


if __name__ == '__main__':
    main()
