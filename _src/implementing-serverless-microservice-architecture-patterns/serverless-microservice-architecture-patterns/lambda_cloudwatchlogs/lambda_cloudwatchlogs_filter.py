"""
Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.


Created on 21 Apr 2018
@author: Richard Freeman

This Lambda filters CloudTrail events for suspicious activities.

"""
from __future__ import print_function


def print_exception(e):
    print(''.join(['Exception ', str(type(e))]))
    print(''.join(['Exception ', str(e.__doc__)]))
    print(''.join(['Exception ', str(e.message)]))


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def filter_cloudwatchlogs_records(event):
        try:
            print(str(event))
            return 'done'

        except Exception as e:
            print_exception(e)
            return


def lambda_handler(event, context):
    response = Controller.filter_cloudwatchlogs_records(event)
    return response
