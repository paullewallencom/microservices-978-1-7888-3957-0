#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

#This Script creates a Lambda role and attaches the policy required

#Settings
. ./common-variables.sh

#Setup Lambda Role
role_name=lambda-sqs
aws iam create-role --role-name ${role_name} \
    --assume-role-policy-document file://../../IAM/assume-role-lambda.json --profile $profile || true

sleep 1
#Create and attach SQS Policy for Lambda
sqs_policy=sqs-full-access-all
aws iam create-policy --policy-name $sqs_policy --policy-document file://../../IAM/$sqs_policy.json --profile $profile || true

role_policy_arn="arn:aws:iam::$aws_account_id:policy/$sqs_policy"
echo $role_policy_arn
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true
	
#Create and attach CloudWatch Policy for Lambda
cloudwatch_policy=lambda-cloud-write
aws iam create-policy --policy-name $cloudwatch_policy --policy-document file://../../IAM/$cloudwatch_policy.json --profile $profile || true

role_policy_arn="arn:aws:iam::$aws_account_id:policy/$cloudwatch_policy"
echo $role_policy_arn
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true
