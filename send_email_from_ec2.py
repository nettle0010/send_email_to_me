#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3

import settings
from send_email_to_me import aws_util

if __name__ == '__main__':
    s3 = boto3.resource('s3')
    attach_file, attach_file_name = aws_util.get_attach_file_from_s3(s3,
                                                                     settings.AWS_S3_BUCKET_NAME,
                                                                     settings.PREFIX_TARGET)
    ses = boto3.client('ses', region_name=settings.AWS_SES_REGION_NAME)
    msg = aws_util.make_mime(settings.MAIL_FROM_ADDR,
                             settings.MAIL_SUBJECT,
                             settings.MAIL_BODY,
                             attach_file,
                             attach_file_name)
    responses = aws_util.send_email(ses,
                                    settings.MAIL_FROM_ADDR,
                                    settings.MAIL_TO_ADDRS,
                                    msg)
