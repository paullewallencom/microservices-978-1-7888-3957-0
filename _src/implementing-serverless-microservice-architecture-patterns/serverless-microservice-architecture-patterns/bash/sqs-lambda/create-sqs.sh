#!/usr/bin/env bash
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

. ./common-variables.sh

aws sqs create-queue \
  --queue-name event-queue \
  --attributes \
      MaximumMessageSize=262144,MessageRetentionPeriod=1209600  \
  --profile $profile --region $region