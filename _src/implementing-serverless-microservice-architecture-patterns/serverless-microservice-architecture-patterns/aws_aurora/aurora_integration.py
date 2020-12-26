#!/usr/bin/python
"""
Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.

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



"""
from __future__ import print_function
import logging
import pymysql
import aurora_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuroraRepository:
    def __init__(self):
        self.conn = pymysql.connect(aurora_config.db_endpoint,
                                    db=aurora_config.db_name,
                                    port=aurora_config.db_port,
                                    user=aurora_config.db_username,
                                    password=aurora_config.db_password,
                                    connect_timeout=aurora_config.db_timeout)
        if self.conn is None:
            logger.error("Error RDS PostgreSQL Connection failed, connection string is None")

        logger.info("RDS PostgreSQL connection successful")
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
            cur.execute("create table IF NOT EXISTS Employee ( EmployeeID  int NOT NULL, \
                        Name varchar(255) NOT NULL, \
                        PRIMARY KEY (EmployeeID))")
            self.conn.commit()

    def insert_row(self, insert_values):
        with self.conn.cursor() as cur:
            cur.execute('INSERT INTO Employee (EmployeeID, Name) VALUES(%s, "%s")' %
                        (insert_values['EmployeeID'],
                         insert_values['Name']))
            self.conn.commit()

    def replace_row(self, insert_values):
        with self.conn.cursor() as cur:
            cur.execute('REPLACE INTO Employee (EmployeeID, Name) VALUES(%s, "%s")' %
                        (insert_values['EmployeeID'],
                         insert_values['Name']))
            self.conn.commit()

    def select_rows(self, limit_row_count=10):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM Employee LIMIT %s" % limit_row_count)
            for row in cur:
                logger.info(row)


repo = AuroraRepository()


def main():
    insert_values = {'EmployeeID': 20, 'Name': "John"}
    repo.replace_row(insert_values)
    # insert_values = {'EmployeeID': 21, 'Name': "Jane"}
    # repo.insert_row(insert_values)
    repo.select_rows(limit_row_count=10)


if __name__ == '__main__':
    main()
