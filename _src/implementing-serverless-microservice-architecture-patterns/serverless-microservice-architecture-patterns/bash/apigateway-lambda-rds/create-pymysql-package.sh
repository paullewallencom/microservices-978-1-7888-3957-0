#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

# This script creates pymysql packages and copies them to the lambda folder
# so that it can be packaged and deployed on AWS
# Run with sudo ./create-pymysql-package.sh

(mkdir ~/tmp;
cd ~/tmp;
virtualenv lambda_package;
cd lambda_package/;
source bin/activate;
pip install --upgrade pip;
pip install pymysql -t lib/python2.7/site-packages/ --upgrade;
ls lib/python2.7/site-packages/pymysql;
#deactivate;
)
rm ../../lambda_aurora/pymysql -R || true
mv ~/tmp/lambda_package/lib/python2.7/site-packages/pymysql ../../lambda_aurora