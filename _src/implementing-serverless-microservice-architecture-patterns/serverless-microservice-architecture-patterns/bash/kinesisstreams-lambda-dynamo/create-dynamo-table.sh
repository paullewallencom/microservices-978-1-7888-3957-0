#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

. ./common-variables.sh
aws dynamodb create-table \
  --table-name user-visits \
  --attribute-definitions \
      AttributeName=EventId,AttributeType=S \
  --key-schema \
      AttributeName=EventId,KeyType=HASH \
  --provisioned-throughput \
      ReadCapacityUnits=1,WriteCapacityUnits=1 \
  --sse-specification Enabled=true \
  --profile $profile \
  --region $region
  