#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

export profile="demo"
export region="eu-west-1"
export aws_account_id="000000000000"
export template="lambda-mysql-secure-api"
export bucket="testbucket121f"
export prefix="tmp/sam"
export user="adm1nuser"
export pass="your-secret-pa55!"
IP=$(curl checkip.amazonaws.com)
export cidrip="$IP/32"
export vpcid="vpc-18b0387e"
