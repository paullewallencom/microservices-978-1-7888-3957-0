#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

# This script creates an aurora cluster then an instance
# It is recommended that you change the username and password 
# for the Lamdba
. ./common-variables.sh
echo "Creating an Aurora Cluster"
clustername=aurora-cluster-wolf-vpc
db_subnet_group_name=wolf-db-subnet

aws rds create-db-cluster \
    --db-cluster-identifier $clustername \
    --engine aurora-mysql \
    --database-name dev \
    --master-username $user \
    --master-user-password $pass \
	--db-subnet-group-name $db_subnet_group_name \
    --backup-retention-period 1 \
    --source-region $region \
    --profile $profile \
    --region $region \
    || true

echo "Creating an Aurora Instance"
aws rds create-db-instance \
    --db-instance-identifier aurora-wolf-vpc \
    --db-cluster-identifier $clustername \
    --db-instance-class db.t2.small \
    --engine aurora-mysql \
    --publicly-accessible \
	--no-multi-az \
    --profile $profile \
    --region $region || true
