#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

# This script creates pymysql packages and copies them to the lambda folder
# so that it can be packaged and deployed on AWS
# Run with sudo ./create-pymysql-package.sh
echo "NEED TO RUN with SUDO:"
echo "sudo ./create-pymysql-package.sh"
(mkdir ~/tmp;
cd ~/tmp;
virtualenv lambda_package;
cd lambda_package/;
source bin/activate;
pip install --upgrade pip;
pip install aws-xray-sdk -t lib/python2.7/site-packages/ --upgrade;
pip install wrapt -t lib/python2.7/site-packages/ --upgrade;
pip install jsonpickle -t lib/python2.7/site-packages/ --upgrade;
pip install pkg_resources -t lib/python2.7/site-packages/ --upgrade;
ls lib/python2.7/site-packages
#deactivate;
)
rm ../../lambda_dynamo_xray/aws_xray_sdk -R || true
mv ~/tmp/lambda_package/lib/python2.7/site-packages/aws_xray_sdk ../../lambda_dynamo_xray
rm ../../lambda_dynamo_xray/wrapt -R || true
mv ~/tmp/lambda_package/lib/python2.7/site-packages/wrapt ../../lambda_dynamo_xray
rm ../../lambda_dynamo_xray/jsonpickle -R || true
mv ~/tmp/lambda_package/lib/python2.7/site-packages/jsonpickle ../../lambda_dynamo_xray
rm ../../lambda_dynamo_xray/pkg_resources -R || true
mv ~/tmp/lambda_package/lib/python2.7/site-packages/pkg_resources ../../lambda_dynamo_xray