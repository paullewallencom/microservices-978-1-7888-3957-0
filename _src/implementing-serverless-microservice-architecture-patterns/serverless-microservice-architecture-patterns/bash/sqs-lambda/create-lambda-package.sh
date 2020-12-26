#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

# This script creates a Zip package of the Lambda files

zip_file="lambda-sqs.zip"
files="lambda_process_sqs_messages.py"

#Create Lambda package and exclude the tests to reduce package size
(cd ../../lambda_sqs_process;
chmod 755 ${files};
mkdir -p ../package/
zip -FSr ../package/"${zip_file}" ${files} -x *tests/*)

