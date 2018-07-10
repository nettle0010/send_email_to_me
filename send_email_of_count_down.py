#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime

import boto3

import settings
from send_email_to_me import util
from send_email_to_me import aws_util

if __name__ == '__main__':
    args = sys.argv
    str_date_to = args[1]
    mail_from_addr = args[2]
    mail_to_addrs = args[3]
    mail_subject = args[4]
    date_from = datetime.datetime.now()
    days_left = util.get_days_left(date_from, str_date_to)
    days_off = util.get_days_off(date_from, str_date_to)
    mail_body = \
        mail_subject + ' まで ' + str(days_left) + ' 日です。' + \
        'それまでに ' + str(days_off) + ' 日の休日があります。（有給休暇を除く）'
    ses = boto3.client('ses', region_name=settings.AWS_SES_REGION_NAME)
    msg = aws_util.make_mime(mail_from_addr,
                             mail_subject,
                             mail_body)
    responses = aws_util.send_email(ses,
                                    mail_from_addr,
                                    mail_to_addrs,
                                    msg)
