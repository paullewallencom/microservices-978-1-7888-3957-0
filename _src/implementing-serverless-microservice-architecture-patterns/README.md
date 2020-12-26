Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0 or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

# Implementing Serverless Microservices Architecture Patterns

## Course Summary

Companies like Netflix, Amazon, and more and more organization are adopting microservices architecture in their products as they allow development teams to work independently on smaller, loosely coupled and simpler services that can be quickly be iterated upon and released into production more frequently, compared to older monolithic approaches. Implementing Serverless Microservices Architecture Patterns aims to show you how to implement over 15 of the most popular microservice patterns using Serverless computing instead of the typically used containers which have costs and maintenance drawbacks. In this course we focus on Serverless computing on AWS, where we walkthrough how these patterns can be implemented more rapidly, with less code and having AWS manage most of the infrastructure and scalability, than container-based microservices. 

We have created original content and architectures that use serverless microservice patterns related to non-relational databases, relational databases, event sourcing, command query responsibility segregation (CQRS), messaging, API composition, monitoring, observability, continuous integration and continuous delivery pipelines. By the end of the course, you’ll be able to build, test, deploy, scale and monitor your microservices with ease using Serverless computing in a continuous delivery pipeline.


## Assumed Knowledge
To fully benefit from the coverage included in this course, you will need:

* Prior working knowledge of programming languages such as Python, node.js, C#, Java, GO
* (Optional) Familiarity with Git and GitHub for source control
* (Optional) Experience with REST APIs, microservices and AWS

## Exercise and Sample Files:

A subset of the course containing the serverless microservice data API is Available on GitHub
The full code, configuration, and shell scripts are available in `implementing-serverless-microservice-architecture-patterns.zip` file with the followingL

* `README.md` – This file
* `serverless-microservice-architecture-patterns` – the main configuration and code repository for section 2, 3, 4 and 5.
    * Section 2 – DynamoDB
    * Section 3 – RDS MySQL, RDS Aurora, and Aurora Serverless
    * Section 4 – Kinesis Streams, DynamoDB Streams, Kinesis Firehose, SQS 
    * Section 5 – CloudWatch Metrics, Logs, Triggers and X-Ray
* `serverless-data-api-deployment-pipeline` – the repo used in section 6 for CI/CD
* `serverless-data-api-lambda-test` – the repo used in section 6 for CI/CD Lambda Testing
