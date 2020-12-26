"""
Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). 
You may not use this file except in compliance with the License. 
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed 
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
express or implied. See the License for the specific language governing 
permissions and limitations under the License.

Created on 10 Apr 2018

@author: Richard Freeman

"""
import json
import logging
from lambda_sqs_process import lambda_process_sqs_messages

logger = logging.getLogger(__name__)

response = lambda_process_sqs_messages.lambda_handler(None, None)
logger.info("Response: %s \n" % json.dumps(response))
