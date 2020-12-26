#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

# This script creates a aurora cluster then an instance

. ./common-variables.sh
clustername=aurora-cluster-secure-wolf-vpc
db_subnet_group_name=wolf-db-subnet

echo "creating an Aurora Cluster"
aws rds create-db-cluster \
    --db-cluster-identifier $clustername \
    --engine aurora-mysql \
    --database-name dev \
    --master-username $user \
    --master-user-password $pass \
	--db-subnet-group-name $db_subnet_group_name \
    --enable-iam-database-authentication \
    --storage-encrypted \
    --backup-retention-period 1 \
    --source-region $region \
    --profile $profile \
    --region $region \
    || true

echo "Creating a Secure Aurora Instance"
aws rds create-db-instance \
    --db-instance-identifier aurora-secure-wolf-vpc \
    --db-cluster-identifier $clustername \
    --db-instance-class db.t2.medium \
    --engine aurora-mysql \
    --publicly-accessible \
    --no-multi-az \
    --profile $profile \
    --region $region || true

#change to --no-publicly-accessible if not using IAM Authentication