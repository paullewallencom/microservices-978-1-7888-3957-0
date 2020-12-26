#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

#This Script creates a Lambda role and attaches the policy required

#Settings
. ./common-variables.sh

###########################################
#Setup codepipeline Role
role_name=codepipeline-serverless
aws iam create-role --role-name ${role_name} \
    --assume-role-policy-document file://../../IAM/assume-role-codepipeline.json --profile $profile || true

sleep 1

#Add and attach Policy for codepipeline
cloudwatch_policy=code-pipeline-policy
aws iam create-policy --policy-name $cloudwatch_policy --policy-document file://../../IAM/$cloudwatch_policy.json --profile $profile || true

role_policy_arn="arn:aws:iam::$aws_account_id:policy/$cloudwatch_policy"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true
	
###########################################
#Setup CodeBuild Role
role_name=codebuild-serverless-service-role
aws iam create-role --role-name ${role_name} \
    --assume-role-policy-document file://../../IAM/assume-role-codebuild.json --profile $profile || true

sleep 1

#Add and attach lambda-full Policy for codebuild
cloudwatch_policy=lambda-full
aws iam create-policy --policy-name $cloudwatch_policy --policy-document file://../../IAM/$cloudwatch_policy.json --profile $profile || true

role_policy_arn="arn:aws:iam::$aws_account_id:policy/$cloudwatch_policy"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true
	
#Add and attach iam-pass-role Policy for codebuild
cloudwatch_policy=iam-pass-role
aws iam create-policy --policy-name $cloudwatch_policy --policy-document file://../../IAM/$cloudwatch_policy.json --profile $profile || true

role_policy_arn="arn:aws:iam::$aws_account_id:policy/$cloudwatch_policy"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true
	
	
##Attach S3 Read Policy
role_policy_arn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true
	
##Attach API Gateway Read Policy
role_policy_arn="arn:aws:iam::aws:policy/AmazonAPIGatewayAdministrator"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true	
		
#Add and attach cloudformation Policy for codepipeline
cloudwatch_policy=cloudformation-full
aws iam create-policy --policy-name $cloudwatch_policy --policy-document file://../../IAM/$cloudwatch_policy.json --profile $profile || true

role_policy_arn="arn:aws:iam::$aws_account_id:policy/$cloudwatch_policy"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true
	
##Attach Lambda deploy Policy
role_policy_arn="arn:aws:iam::aws:policy/service-role/AWSCodeDeployRoleForLambda"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true	
	
#Add and attach codebuild Policy
cloudwatch_policy=codebuild-base
aws iam create-policy --policy-name $cloudwatch_policy --policy-document file://../../IAM/$cloudwatch_policy.json --profile $profile || true

role_policy_arn="arn:aws:iam::$aws_account_id:policy/$cloudwatch_policy"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true	

#Add codecommit Git Pull 
codecommit_policy=codecommit-git-pull
aws iam create-policy --policy-name $codecommit_policy --policy-document file://../../IAM/$codecommit_policy.json --profile $profile || true

role_policy_arn="arn:aws:iam::$aws_account_id:policy/$codecommit_policy"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true	


##Attach DynamoDB Policy
role_policy_arn="arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true	
	
###########################################
#Setup CloudFormation Role
role_name=cloudformation-lambda-execution-role
aws iam create-role --role-name ${role_name} \
    --assume-role-policy-document file://../../IAM/assume-role-cloudformation.json --profile $profile || true

sleep 1

#Add and attach cloudformation Policy for codepipeline
cloudwatch_policy=cloudformation-full
aws iam create-policy --policy-name $cloudwatch_policy --policy-document file://../../IAM/$cloudwatch_policy.json --profile $profile || true

role_policy_arn="arn:aws:iam::$aws_account_id:policy/$cloudwatch_policy"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true
	
#Add and attach Policy for codepipeline
cloudwatch_policy=cloudormation-build-pipeline
aws iam create-policy --policy-name $cloudwatch_policy --policy-document file://../../IAM/$cloudwatch_policy.json --profile $profile || true

role_policy_arn="arn:aws:iam::$aws_account_id:policy/$cloudwatch_policy"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true
	
##Attach DynamoDB Policy
role_policy_arn="arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true
	
##Attach Lambda Policy
role_policy_arn="arn:aws:iam::aws:policy/AWSLambdaExecute"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true

