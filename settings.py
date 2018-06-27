#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

AWS_S3_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME')
AWS_SES_REGION_NAME = os.environ.get('AWS_SES_REGION_NAME')
MAIL_FROM_ADDR = os.environ.get('MAIL_FROM_ADDR')
MAIL_TO_ADDRS = os.environ.get('MAIL_TO_ADDRS')
MAIL_SUBJECT = os.environ.get('MAIL_SUBJECT')
MAIL_BODY = os.environ.get('MAIL_BODY')
PREFIX_TARGET = os.environ.get('PREFIX_TARGET')