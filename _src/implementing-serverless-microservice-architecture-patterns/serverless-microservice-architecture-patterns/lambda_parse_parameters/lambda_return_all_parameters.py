"""
Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.

Created on 31 Dec 2017

@author: Richard Freeman

Extracts the resource_id and URL parameter, and returns them 
as a valid response payload.

"""

import json


def respond(err=None, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def parse_parameters(event):
    try:
        return_parameters = event['queryStringParameters'].copy()
    except Exception as e:
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


def lambda_handler(event, context):
    # print (str(event)) #Useful to create sample data
    validated_parameters = parse_parameters(event)
    if validated_parameters["err"] is not None:
        return respond(validated_parameters['err'])
    else:
        return respond(err=None, res=validated_parameters.get('parsedParams'))
