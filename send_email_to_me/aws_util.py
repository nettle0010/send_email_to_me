#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import botocore


def get_attach_file_from_s3(s3, bucket_name, prefix_target):
    attach_file = None
    attach_file_name = ''
    try:
        bucket = s3.Bucket(bucket_name)
        # get all file names
        file_names = [obj_summary.key.split('/')[-1] for obj_summary in bucket.objects.all()
                      if obj_summary.key.startswith(prefix_target) and len(obj_summary.key.split('/')[-1]) != 0]
        attach_file_name = random.choice(file_names)
        obj = bucket.Object(prefix_target + attach_file_name)
        response = obj.get()
        attach_file = response['Body'].read()
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])
    return attach_file, attach_file_name
