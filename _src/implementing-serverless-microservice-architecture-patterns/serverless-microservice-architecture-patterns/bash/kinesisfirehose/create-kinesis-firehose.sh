#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

. ./common-variables.sh
aws firehose create-delivery-stream \
  --delivery-stream-name clickstream-metrics \
  --delivery-stream-type DirectPut \
  --extended-s3-destination-configuration RoleARN=arn:aws:iam::$aws_account_id:role/kinesis-firehose-s3-role,BucketARN=arn:aws:s3:::$bucket,Prefix=firehose/,BufferingHints={SizeInMBs=60,IntervalInSeconds=60},CompressionFormat=UNCOMPRESSED,CloudWatchLoggingOptions={Enabled=true,LogGroupName=firehose,LogStreamName=metrics} \
  --profile $profile \
  --region $region
  