#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

# This script creates a Zip package of the Lambda files

zip_file="lambda-dynamo-xray.zip"
packages="aws_xray_sdk wrapt jsonpickle pkg_resources"
files="lambda_return_dynamo_records.py"

#Create Lambda package and exclude the tests to reduce package size
(cd ../../lambda_dynamo_xray;
chmod 755 ${files};
mkdir -p ../package/
zip -FSr ../package/"${zip_file}" ${packages} ${files} -x *tests/*;
ls -l ../package/"${zip_file}")

