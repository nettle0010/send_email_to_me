#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formatdate

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


def make_mime(mail_from_addr, mail_subject, mail_body, attach_file=None, attach_file_name=''):
    msg = MIMEMultipart()
    msg['From'] = mail_from_addr
    msg['Subject'] = mail_subject
    msg['Date'] = formatdate()

    msg.attach(MIMEText(mail_body.encode('UTF-8'), 'plain', 'UTF-8'))

    if attach_file is not None and len(attach_file_name) > 0:
        part = MIMEApplication(attach_file, filename=attach_file_name)
        part.add_header('Content-Disposition', 'attachment', filename=attach_file_name)
        msg.attach(part)
    return msg


def send_email(ses, mail_from_addr, mail_to_addrs, msg):
    responses = []
    for mail_to_addr in mail_to_addrs.split(','):
        msg['To'] = mail_to_addr
        try:
            response = ses.send_raw_email(
                Source=mail_from_addr,
                Destinations=[mail_to_addr],
                RawMessage={'Data': msg.as_string()}
            )
            responses.append(response)
        except botocore.exceptions.ClientError as e:
            print(e.response['Error']['Message'])
    return responses
