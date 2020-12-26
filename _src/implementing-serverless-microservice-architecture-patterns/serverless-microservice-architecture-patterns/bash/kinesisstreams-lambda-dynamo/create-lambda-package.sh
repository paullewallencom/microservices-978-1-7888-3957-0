#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

# This script creates a Zip package of the Lambda files

. ./common-variables.sh

#Create Lambda package and exclude the tests to reduce package size
(cd ../../lambda_kinesis_visits_metrics;
chmod 755 ${source_files};
mkdir -p ../package/
zip -FSr ../package/"${zip_file}"  ${source_files} -x *tests/*;
ls -l ../package/"${zip_file}")

