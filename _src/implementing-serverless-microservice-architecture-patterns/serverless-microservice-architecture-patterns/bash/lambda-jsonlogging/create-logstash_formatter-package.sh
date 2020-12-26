#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

echo "This script creates logstash_formatter packages and copies them to the lambda folder"
echo "so that it can be packaged and deployed on AWS"
# Run with sudo ./create-logstash_formatter-package.sh if get Permission denied use chmod +x
echo "Run with SUDO"
echo "sudo ./create-logstash_formatter-package.sh"
(mkdir ~/tmp;
cd ~/tmp;
virtualenv lambda_package;
cd lambda_package/;
source bin/activate;
pip install --upgrade pip;
pip install logstash_formatter -t lib/python2.7/site-packages/ --upgrade;
ls lib/python2.7/site-packages/logstash_formatter;
#deactivate;
)
rm ../../lambda_logging/logstash_formatter -R || true
mv ~/tmp/lambda_package/lib/python2.7/site-packages/logstash_formatter ../../lambda_logging