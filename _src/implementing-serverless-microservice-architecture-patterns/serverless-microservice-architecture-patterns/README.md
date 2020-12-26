Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0 or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

## Serverless Microservice Architecture Patterns

In this repository, I code and configuration scripts used to test, secure, build, package, and deploy serverless microservices architecture patterns. This includes the IAM Roles and Policy creation, SAM templates, and resource creation such as SQS, Kinesis Stream, Kinesis Firehose, and DynamoDB.


### 1. Project Structure:

Unzip the `implementing-serverless-microservice-architecture-patterns.zip` and change directory to `serverless-microservice-architecture-patterns`

The folder structure is as follows:
* `bash` - includes all the shell scripts. Each folder includes the integration, e.g. `apigateway-lambda-dynamodb` means API Gateway is integrated with Lambda which talks to DynamoDB
* `IAM` - included all the IAM policies used by the `./create-role.sh` scripts for each pattern
* `sample_data`- includes sample DynamoDB, and JSON event sources for testing API Gateway and Lambda functions
* `test` - unit test and run local code
* other folders - Python Lambda (prefixed with `lambda`) and AWS resource helper code (prefixed with `aws`)


### 2. Windows Only

A lot can be done with the web interface in the AWS Management console, but most often that is time consuming, repetitive and prone to error, and not recommended for production deployments. What is accepted as best practice is to deploy and manage your infrastructure using code and configuration only.

Using bash makes your life much easier when deploying and managing you serverless stack. I think all analysts, data scientists, architects, administrators, DBAs, developers, DevOps and technical people should know some basic bash and be able to run shell scripts, which are typically used on LINUX and UNIX (including macOS Terminal).

Alternatively you can adapt the scripts to use MS-DOS or Powershell but it's not something I recommended, given that bash can now run natively on Windows 10+ as a feature.

Note that I have stripped off the `\r` or carriage returns, as they are illegal in shell scripts, so use notepad++ on Windows if you want to view files properly!

Install Bash for Windows:

* Control Panel > Programs > Turn Windows Features On Or Off. 
* Enable the `Windows Subsystem for Linux` option in the list, and then click the `OK` button.
* Select Ubuntu
* [Detailed guide](https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/)

### 3. Update Ubuntu and Install Git
Git will be used in Section 6
```
$ sudo apt-get update
$ sudo apt-get -y upgrade
$ apt-get install git-core

```

### 3. Install Python and Dependencies

The Lambda code uses Python 2.7. Pip is a tool for installing and managing Python packages. The packages required for the severless data API are listed in  `requirements.txt` and can be installed using pip

```
$ apt-get -y install python2.7 python-pip
$ sudo pip install -r requirements.txt
```

### 4. Install and Setup AWS CLI

You will need to create a user, AWS keys, and enter them them running aws configure. more details are available in [AWS Docs](https://docs.aws.amazon.com/lambda/latest/dg/setup-awscli.html) or my courses.

```
$ pip install awscli --upgrade --user
$ aws configure
```

### 5. Update AccountId, Bucket and Profile for each Pattern
Here I assume your AWS profile is `demo` you can change that under `common-variables.sh`. 
You will need to use a bucket or create one if you haven't already:
```
$ aws s3api create-bucket --bucket mynewbucket231 --profile demo --create-bucket-configuration LocationConstraint=eu-west-1 --region eu-west-1
```
You will also need to change the AWS accountId (current set to 000000000000). The AWS accountId is also used in some IAM policies in the IAM folder. In addition the region will have to be changed.

to replace your accountId (assume your AWS accountId is 111111111111) you can do it manually or run:
```
find ./ -type f -exec sed -i '' -e 's/000000000000/111111111111/' {} \;
```

## Example Lambda Dynamo X-Ray test, build, and deployment

Here is a detailed walk though similar to what I show in the videos.
The other patterns are very similar but with different resources / steps.

### 1. Modify common-variables.sh
Change directory to the main bash folder for the pattern
```
$ cd bash/lambda-dynamo-xray/
$ vi common-variables.sh
```
Change the `profile`, `region`, `bucket`, and `aws_account_id` (`aws_account_id` should have been changed in the last step with `sed`) to make sure they match your current environment setup.

### 2. Add external dependencies to Lambda source
```
$ sudo ./create-aws-xray-sdk-package.sh
```
It's important that you use `SUDO` for this shell script, otherwise it will fail.
You should now see four new sub-folders under `lambda_dynamo_xray`:

* aws_xray_sdk
* jsonpickle
* pkg_resources
* wrapt

The same step is needed for JSON Logging and MySQL/Aurora stacks, as the packages are not natively included with Python. This shell script can be adapted for your requirements, it uses venv so will not impact your local environment.


### 3. Build Package and Deploy the Serverless stack using SAM and CloudFormation.
This also creates the IAM Polices and IAM Roles using the AWS CLI that will be required for the Lambda function. I've done that so that they can easily be shared between Lambda and other resources rather than per Serverless stack.
```
$ ./build-package-deploy-lambda-dynamo.sh
```
 If there are issues the best place to look is the messages in the terminal and the AWS Management Console > CloudFormation > Events

### (Optional) 4. Run Lambda Integration Test
Once the stack is up and running correctly, you can run an integration test to check that the Lambda is working correctly.
```
./invoke-lambda.sh
```

### 5. Add data to DynamoDb table

Run the Python code to add data to the table to make it more realistic, you can also do this under you favourite IDE like PyDev or PyCharm, I have other helpers for querying and inserting rows.
```
$ (cd ../../aws_dynamo; python dynamo_insert_items_from_file_xray.py)
```

### 6. AWS Management Console
Now the stack is up, you can have a look at the API Gateway in the AWS Management Console and test the API in your browser.
* API Gateway > lambda-dynamo-data-api
* Stages > Prod > Get
* Copy the Invoke URL into a new tab, e.g. `https://XXXXXXXXXX.execute-api.eu-west-1.amazonaws.com/Prod/visits/{resourceId}`
* You should get a message `resource_id not a number` as the ID is not valid
* Replace `{resourceId}` with `324`
if all is working you should see some returned JSON records. Well done if so!
Otherwise look at the error messages, CloudFormation stack and ensure your credentials are setup correctly. You can also test the Lambda with some sample data and look at the CloudWatch logs.

### 7. (optional) Run Load Testing
```
(cd ../..; locust -f test/locust_test_script.py --host=https://XXXXXXXXXX.execute-api.eu-west-1.amazonaws.com)
```
Open your browser
http://localhost:8089/

You can simulate the number of users hitting you Data API.
You will see the request latency and useful charts showing requests overtime, change the DynamoDb Read/Write capacity and Lambda RAM to see the effects.

### 8. Deleting the stack
Delete the cloudFormation serverless stack.

```
$ ./delete-lambda-dynamo-data-api.sh
```

Well done you have now been over a complete example!
Have a look at the other bash folders!
