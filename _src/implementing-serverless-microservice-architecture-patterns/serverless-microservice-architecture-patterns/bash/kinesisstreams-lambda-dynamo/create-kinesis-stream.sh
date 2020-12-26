#!/bin/sh
# Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

. ./common-variables.sh

aws kinesis create-stream \
  --stream-name clickstream \
  --shard-count 1 \
  --profile $profile \
  --region $region
  