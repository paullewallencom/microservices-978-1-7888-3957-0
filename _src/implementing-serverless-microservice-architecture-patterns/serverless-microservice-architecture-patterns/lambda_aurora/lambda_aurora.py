#!/usr/bin/python
"""
Copyright (c) 2017-2018 STARWOLF Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). 
You may not use this file except in compliance with the License. 
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed 
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
express or implied. See the License for the specific language governing 
permissions and limitations under the License.

Created on 12 Mar 2018

@author: Richard Freeman

pip install pymysql

This package queries Aurora and MySQL RDS database,
and returns the specified rows as JSON.
"""

import logging
import pymysql
import json
import aurora_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmployeeRepository:
    def __init__(self):
        self.conn = pymysql.connect(aurora_config.db_endpoint,
                                    db=aurora_config.db_name,
                                    port=aurora_config.db_port,
                                    user=aurora_config.db_username,
                                    password=aurora_config.db_password,
                                    connect_timeout=aurora_config.db_timeout)
        if self.conn is None:
            logger.error("Error RDS MySQL Connection failed, connection string is None")

        logger.info("RDS MySQL connection successful")
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
            cur.execute("create table IF NOT EXISTS Employee ( EmployeeID  int NOT NULL, \
                        Name varchar(255) NOT NULL, \
                        PRIMARY KEY (EmployeeID))")
            self.conn.commit()

    def select_rows(self, limit_row_count=10):
        return_payload = []
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM Employee LIMIT %s" % limit_row_count)
            for row in cur:
                return_payload.append(row)
        return return_payload

    def get_employee(self, employee_id=0):
        return_payload = []
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM Employee WHERE EmployeeID = %s" % employee_id)
            for row in cur:
                return_payload.append(row)
        return return_payload

    def replace_employee(self, insert_values):
        try:
            with self.conn.cursor() as cur:
                affected_count = cur.execute('REPLACE INTO Employee (EmployeeID, Name) VALUES(%s, "%s")' %
                                             (insert_values['EmployeeID'],
                                              insert_values['Name']))
                self.conn.commit()
                logging.info("%d", affected_count)
                return {"body": "affected_count: %d" % affected_count, "err": None}
        except Exception as e:
            return {"body": None, "err": e}  # OK for debug, but very bad to expose exception in production


class HttpUtils:
    def __init__(self):
        pass

    @staticmethod
    def respond(err=None, res=None):
        return {
            'statusCode': '400' if err else '200',
            'body': err.message if err else json.dumps(res),
            'headers': {
                'Content-Type': 'application/json',
            },
        }

    @staticmethod
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

    @staticmethod
    def parse_body(event):
        try:
            return {"body": json.loads(event['body']), "err": None}
        except Exception as e:
            return {"body": None, "err": e}


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def process_request(event):
        http_method = event['httpMethod'].lower()
        if http_method == 'get':
            validated_parameters = HttpUtils.parse_parameters(event)
            if validated_parameters["err"] is not None:
                return HttpUtils.respond(validated_parameters['err'])
            else:
                return_payload = repo.get_employee(employee_id=validated_parameters['parsedParams']['resource_id'])
                return HttpUtils.respond(res=return_payload)

        elif http_method == 'put':
            parsed_body = HttpUtils.parse_body(event)
            if parsed_body['err'] is None:
                # Validate payload, e.g.
                if parsed_body['body']['EmployeeID'].isdigit():
                    parsed_body['body']['EmployeeID'] = int(parsed_body['body']['EmployeeID'])
                    return_payload = repo.replace_employee(parsed_body['body'])
                else:
                    return_payload = "EmployeeID Needs to be a digit"
                return HttpUtils.respond(res=return_payload)
            else:
                return HttpUtils.respond(err=parsed_body['err'], res="error processing request")


repo = EmployeeRepository()


def lambda_handler(event, context):
    response = Controller.process_request(event)
    return response
    # print (str(event)) #Useful to create sample data
