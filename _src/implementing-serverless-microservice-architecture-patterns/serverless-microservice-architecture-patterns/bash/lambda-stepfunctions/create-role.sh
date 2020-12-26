#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

#This Script creates a Lambda role and attaches the policy required

#Settings
profile=demo
region=eu-west-1
aws_account_id=000000000000
role_name=lambda-execution-role

cloudwatch_policy=lambda-cloud-write
aws iam create-policy --policy-name $cloudwatch_policy \
    --policy-document file://../../IAM/$cloudwatch_policy.json \
    --profile $profile || true

#Setup Lambda Role
aws iam create-role --role-name ${role_name} \
    --assume-role-policy-document file://../../IAM/assume-role-lambda.json \
    --profile $profile || true

sleep 1

#Add Policy for Lambda
role_policy_arn="arn:aws:iam::$aws_account_id:policy/$cloudwatch_policy"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true
