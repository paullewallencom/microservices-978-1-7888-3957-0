#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

# This script creates a Zip package of the Lambda files

zip_file="lambda-dynamo-data-api.zip"
files="lambda_return_dynamo_records.py"

#Create Lambda package and exclude the tests to reduce package size
(cd ../../lambda_dynamo_read;
chmod 755 ${files};
mkdir -p ../package/
zip -FSr ../package/"${zip_file}" ${files} -x *tests/*)

