#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

# This script creates a Zip package of the Lambda files

zip_file="lambda-mysql-secure.zip"
files="lambda_aurora_secure.py aurora_config_iam.py rds-combined-ca-bundle.pem"

#Create Lambda package and exclude the tests to reduce package size
(cd ../../lambda_aurora_secure;
chmod 755 ${files};
mkdir -p ../package/
zip -FSr ../package/"${zip_file}" pymysql ${files} -x *tests/*;
ls -l ../package/"${zip_file}")

