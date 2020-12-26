#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

#This Script creates a Lambda role and attaches the policy required for it to run in a VPC

#Settings
. ./common-variables.sh

#profile=demo
#region=eu-west-1
#aws_account_id=000000000000
role_name=lambda-vpc-execution-role

#Setup Lambda Role
aws iam create-role --role-name ${role_name} \
    --assume-role-policy-document file://../../IAM/assume-role-lambda.json --profile ${profile}

#Add Policy for Lambda to run in VPC
role_policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile}

#Adding IAM DB Authentication	
rds_auth_policy=rds-iam-db-authentication
aws iam create-policy --policy-name $rds_auth_policy --policy-document file://../../IAM/$rds_auth_policy.json --profile $profile || true

#Add Policy for Lambda
role_policy_arn="arn:aws:iam::$aws_account_id:policy/$rds_auth_policy"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true
