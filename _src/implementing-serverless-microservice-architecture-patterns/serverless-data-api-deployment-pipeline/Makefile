#!/bin/bash
# Copyright (c) 2017-2018 STARWOLF Ltd and Richard Freeman. All Rights Reserved.

TEMPLATE = "lambda-dynamo-data-api"
BUCKET = "testbucket121f"
PREFIX = "sam"
REGION = "eu-west-1"
VENVPATH = "~/tmp/python_lambda_test"

runAllUnitTests:
		echo 'running unit test'
		python -m unittest discover test;

runAllUnitTestsVm: requirements.txt
		mkdir -p ${VENVPATH}
		virtualenv --python=/usr/bin/python2.7 ${VENVPATH}
		(${VENVPATH}/bin/activate; \
		${VENVPATH}/bin/pip install -r $^; \
		python -m unittest discover test;)
		rm -r ${VENVPATH}
		
packageLambdaDataApi: 
		aws cloudformation package --template-file ${TEMPLATE}.yaml --output-template-file ${TEMPLATE}-output.yaml --s3-bucket ${BUCKET} --s3-prefix ${PREFIX} --region ${REGION}

deployLambdaDataApi:
		aws cloudformation deploy --template-file ${TEMPLATE}-output.yaml --stack-name ${TEMPLATE} --capabilities CAPABILITY_IAM --region ${REGION}

deleteStack:
		aws cloudformation delete-stack --stack-name ${TEMPLATE} --region ${REGION}

listLambdas:
		aws lambda list-functions --region ${REGION}
	
runIntegrationTestLambdaDataApi:
		echo "Running integration test"
		( cd bash/apigateway-lambda-dynamodb/ && ./invoke-lambda.sh )
