#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

#This Script creates a Lambda role and attaches the policy required for it to run in a VPC

#Settings
. ./common-variables.sh

role_name=api-gateway-logs-role

#Setup API Gateway Role
aws iam create-role --role-name ${role_name} \
    --assume-role-policy-document file://../../IAM/assume-role-api-gateway.json \
	--profile $profile || true

#Add Policy for API Gateway Execution
role_policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaRole"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  \
	--profile ${profile} || true
	
#Create and attach CloudWatch policy to role
cloudwatch_policy=lambda-cloud-write
aws iam create-policy --policy-name $cloudwatch_policy --policy-document file://../../IAM/$cloudwatch_policy.json --profile $profile || true

role_policy_arn="arn:aws:iam::$aws_account_id:policy/$cloudwatch_policy"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true
