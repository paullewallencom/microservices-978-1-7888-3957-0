#!/usr/bin/env bash
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

# This Shell script orchestrates creating Lambda Zip package,
# packaging and deploying it as a CloudFormation stack

echo "Run sudo ./create-aws-xray-sdk-package.sh first"
#Variables
. ./common-variables.sh

#Create policies and role
./create-role.sh

#Create Zip file of Lambda code and dependencies 
./create-lambda-package.sh

#Package your Serverless Stack using SAM + Cloudformation
aws cloudformation package --template-file $template.yaml --output-template-file ../../package/$template-output.yaml --s3-bucket $bucket --s3-prefix $prefix --region $region --profile $profile

#Deploy your Serverless Stack using SAM + Cloudformation
aws cloudformation deploy --template-file ../../package/$template-output.yaml --stack-name $template --capabilities CAPABILITY_IAM --region $region --profile $profile

#Enable X-ray as not supported in SAM YAML yet:
aws lambda update-function-configuration --function-name lambda-dynamo-xray-sam --tracing-config Mode=Active