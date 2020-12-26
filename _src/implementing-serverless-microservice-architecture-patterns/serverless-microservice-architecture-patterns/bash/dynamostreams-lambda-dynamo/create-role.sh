#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

#This Script creates a Lambda role and attaches the policy required for it to run in a VPC

#import variables
. ./common-variables.sh

role_name=lambda-dynamo-replication-execution-role

#Setup Lambda Role
aws iam create-role --role-name ${role_name} \
	--assume-role-policy-document file://../../IAM/assume-role-lambda.json \
	--profile $profile \
	--region $region || true

#Create Policies
aws iam create-policy --policy-name dynamostreams-readonly-user-visits \
	--policy-document file://../../IAM/dynamostreams-readonly-user-visits.json \
	--profile $profile \
	--region $region || true
	
aws iam create-policy --policy-name dynamo-full-user-visits-replicated \
	--policy-document file://../../IAM/dynamo-full-user-visits-replicated.json \
	--profile $profile \
	--region $region || true
	
#Attach Policies to Role
role_policy_arn="arn:aws:iam::${aws_account_id}:policy/dynamo-full-user-visits-replicated"
aws iam attach-role-policy \
	--role-name "${role_name}" \
	--policy-arn "${role_policy_arn}"  \
	--profile $profile \
	--region $region || true

role_policy_arn="arn:aws:iam::${aws_account_id}:policy/dynamostreams-readonly-user-visits"
aws iam attach-role-policy \
	--role-name "${role_name}" \
	--policy-arn "${role_policy_arn}"  \
	--profile $profile \
	--region $region || true
