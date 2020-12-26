#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

export profile="demo"
export region="eu-west-1"
export aws_account_id="000000000000"
export zip_file="lambda-dynamo-replicator.zip"
export source_files="dynamo_to_dynamo_replicator_simple.py"
export template="lambda-dynamo-replicator"
export bucket=testbucket121f
export prefix=tmp/sam
