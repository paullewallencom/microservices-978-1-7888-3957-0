#!/usr/bin/env bash
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

template=lambda-dynamo-data-api
region=eu-west-1
profile=demo

aws cloudformation delete-stack --stack-name $template --region $region --profile $profile
