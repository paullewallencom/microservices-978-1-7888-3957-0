#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

#This Script creates a Lambda role and attaches the policy required to read from Kines Streams, and for Kinesis Firehose to write to S3

#import variables
. ./common-variables.sh

####################
### Kinesis Firehose Roles
firehose_role_name=kinesis-firehose-s3-role
aws iam create-role --role-name ${firehose_role_name} \
	--assume-role-policy-document file://../../IAM/assume-role-kinesis-firehose.json \
	--profile $profile \
	--region $region || true

#Create Policies
policy_name=kinesis-firehose-s3-full
aws iam create-policy --policy-name $policy_name \
	--policy-document file://../../IAM/$policy_name.json \
	--profile $profile \
	--region $region || true

#Attach policy
role_policy_arn="arn:aws:iam::${aws_account_id}:policy/$policy_name"
aws iam attach-role-policy \
	--role-name "${firehose_role_name}" \
	--policy-arn "${role_policy_arn}"  \
	--profile $profile \
	--region $region || true
