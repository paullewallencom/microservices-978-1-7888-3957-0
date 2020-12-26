#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

# This script creates a MySQL RDS instance
# It is recommended that you change the username and password
# t2.small is the smallest that supports encryption at rest
. ./common-variables.sh

aws rds create-db-instance \
    --db-instance-identifier my-sql-iam \
    --db-instance-class db.t2.small \
    --engine mysql \
    --allocated-storage 5 \
    --publicly-accessible \
    --db-name dev \
    --master-username $user \
    --master-user-password $pass \
    --no-multi-az \
    --enable-iam-database-authentication \
    --storage-encrypted \
    --backup-retention-period 0 \
    --profile $profile \
	--region $region