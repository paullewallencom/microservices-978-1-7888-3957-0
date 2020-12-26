"""
Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). 
You may not use this file except in compliance with the License. 
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed 
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
express or implied. See the License for the specific language governing 
permissions and limitations under the License.

Created on 18 Dec 2017

@author: Richard Freeman

"""

from lambda_kinesis_visits_metrics.lambda_kinesis_visits_metrics import lambda_handler 
import json
import logging


logger = logging.getLogger(__name__)

   
def run_local_kinesis_streams_clickstream():
    print ("running local lambda")
    with open('../sample_data/kinesis-streams-clickstream.json', 'r') as myfile:
        event = myfile.read()
    lambda_handler(json.loads(event), context=None)

    with open('../sample_data/kinesis-streams-clickstream-errors.json', 'r') as myfile:
        event = myfile.read()
    lambda_handler(json.loads(event), context=None)


def main():
   
    run_local_kinesis_streams_clickstream()

    
if __name__ == '__main__':
    main()
