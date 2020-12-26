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
import json
from lambda_aurora import lambda_aurora


def main():
    # with open('../sample_data/request-api-gateway-valid-get-error.json', 'r') as sample_request:
    # with open('../sample_data/request-api-gateway-valid-get.json', 'r') as sample_request:
    # with open('../sample_data/request-api-gateway-valid-put-error.json', 'r') as sample_request:

    with open('../sample_data/request-api-gateway-valid-put.json', 'r') as sample_request:
        event = json.loads(sample_request.read())
    print("Using data: " + str(event))
    print(sample_request.name.split('/')[-1])
    response = lambda_aurora.lambda_handler(event, None)
    print("Response: %s \n" % json.dumps(response))


if __name__ == '__main__':
    main()
