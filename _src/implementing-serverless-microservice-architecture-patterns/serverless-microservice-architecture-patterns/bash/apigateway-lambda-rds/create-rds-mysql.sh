#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

# This script creates a MySQL RDS instance
# It uses Default VPC
# It is recommended that you change the username and password
. ./common-variables.sh

aws rds create-db-instance \
    --db-instance-identifier mysql-default-vpc \
    --db-instance-class db.t2.micro \
    --engine mysql \
    --allocated-storage 5 \
    --no-publicly-accessible \
    --db-name dev \
    --master-username $user \
    --master-user-password $pass \
    --backup-retention-period 0 \
    --profile $profile \
    --region $region
