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

This package sends records to Kinesis Streams

"""

import boto3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def put_record(stream_name, data, partition_key, region='eu-west-1'):
    client = boto3.client(service_name='kinesis', region_name=region)
    response = client.put_record(
        StreamName=stream_name,
        Data=data,
        PartitionKey=partition_key
    )
    logging.info(response)


def put_sample_record(region='us-east-1'):
    stream_name = 'clickstream-sam'
    data = """{"user_id":"SD23hj32!",
                "user_agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36.",
                "referer":"https://www.google.com/",
                "url":"https://www.mysite.com/timeline", 
                "event_name":"page view",
                "page_id":"200"
              }
           """
    partition_key = "SD23hj32!"
    put_record(stream_name=stream_name, data=data,
               partition_key=partition_key, region=region)


def main():
    region = 'eu-west-1'
    put_sample_record(region=region)


if __name__ == '__main__':
    main()
