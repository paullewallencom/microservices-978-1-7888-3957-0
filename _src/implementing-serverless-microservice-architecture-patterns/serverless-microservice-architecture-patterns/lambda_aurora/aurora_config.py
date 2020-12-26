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

I recommend that these details are encrypted using KMS
and provided as environment variables

@author: Richard Freeman
"""
db_username = "adm1nuser"
db_password = "your-secret-pa55!"
db_name = "dev"
#db_endpoint = "my-sql-iam.XXXXXXXXXXXX.eu-west-1.rds.amazonaws.com"
db_endpoint = "aurora-cluster.cluster-XXXXXXXXXXXX.eu-west-1.rds.amazonaws.com"
db_port = 3306
db_timeout = 5
