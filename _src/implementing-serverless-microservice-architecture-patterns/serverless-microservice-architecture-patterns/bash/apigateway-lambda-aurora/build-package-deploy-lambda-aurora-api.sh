#!/usr/bin/env bash
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.

# This Shell script orchestrates creating Lambda Zip package,
# packaging and deploying it as a CloudFormation stack

#Import Variables
. ./common-variables.sh

#Create the roles needed by API Gateway and Lambda
./create-role.sh

#Create Zip file of Lambda code and dependencies 
./create-lambda-package.sh

#Package your Serverless Stack using SAM + Cloudformation
aws cloudformation package --template-file $template.yaml --output-template-file ../../package/$template-output.yaml --s3-bucket $bucket --s3-prefix $prefix --region $region --profile $profile

#Deploy your Serverless Stack using SAM + Cloudformation
aws cloudformation deploy --template-file ../../package/$template-output.yaml --stack-name $template --capabilities CAPABILITY_IAM --region $region --profile $profile