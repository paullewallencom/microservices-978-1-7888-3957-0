#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

#This Script creates a Lambda role and attaches the policy required to read from Kines Streams and write the metrics to DynamoDB

#import variables
. ./common-variables.sh

#Setup Lambda Role
role_name=lambda-kinesis-dynamo-execution-role
aws iam create-role --role-name ${role_name} \
	--assume-role-policy-document file://../../IAM/assume-role-lambda.json \
	--profile $profile \
	--region $region || true

#Create and Attach Kinesis Streams policy 
aws iam create-policy --policy-name kinesis-streams-get-clickstream \
	--policy-document file://../../IAM/kinesis-streams-get-clickstream.json \
	--profile $profile \
	--region $region || true

role_policy_arn="arn:aws:iam::${aws_account_id}:policy/kinesis-streams-get-clickstream"
aws iam attach-role-policy \
	--role-name "${role_name}" \
	--policy-arn "${role_policy_arn}"  \
	--profile $profile \
	--region $region || true

#Create and Attach DynamoDB Policy to Role	
aws iam create-policy --policy-name dynamo-full-user-visits \
	--policy-document file://../../IAM/dynamo-full-user-visits.json \
	--profile $profile \
	--region $region || true
	
role_policy_arn="arn:aws:iam::${aws_account_id}:policy/dynamo-full-user-visits"
aws iam attach-role-policy \
	--role-name "${role_name}" \
	--policy-arn "${role_policy_arn}"  \
	--profile $profile \
	--region $region || true
	
#Create and attach CloudWatch policy to role
cloudwatch_policy=lambda-cloud-write
aws iam create-policy --policy-name $cloudwatch_policy --policy-document file://../../IAM/$cloudwatch_policy.json --profile $profile || true

role_policy_arn="arn:aws:iam::$aws_account_id:policy/$cloudwatch_policy"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true
