#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest

from io import StringIO

import boto3

from moto import mock_s3
from moto import mock_ses

from send_email_to_me import aws_util


class TestAwsUtil(unittest.TestCase):
    def setUp(self):
        self.captor = StringIO()
        sys.stdout = self.captor

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @mock_s3
    def test_get_attach_file_from_s3(self):
        s3 = boto3.resource('s3')
        attach_file, attach_file_name = aws_util.get_attach_file_from_s3(s3,
                                                                         'mybucket',
                                                                         'myfolder/')
        self.assertEqual(self.captor.getvalue(), 'The specified bucket does not exist\n')

        client = boto3.client('s3')
        client.create_bucket(Bucket='mybucket')
        data = open('tests/test.jpg', 'rb')
        client.put_object(Bucket='mybucket',Key='myfolder/test.jpg', Body=data)
        data.close()
        attach_file, attach_file_name = aws_util.get_attach_file_from_s3(s3,
                                                                         'mybucket',
                                                                         'myfolder/')
        data = open('tests/test.jpg', 'rb')
        self.assertEqual(attach_file, data.read())
        data.close()
        self.assertEqual(attach_file_name, 'test.jpg')

    def test_make_mime(self):
        msg = aws_util.make_mime('test@example.com',
                                 'test_subject',
                                 'test_body')
        self.assertTrue(msg.is_multipart())
        self.assertEqual(msg['From'], 'test@example.com')
        self.assertEqual(msg['Subject'], 'test_subject')
        data = open('tests/test.jpg', 'rb')
        msg = aws_util.make_mime('test@example.com',
                                 'test_subject',
                                 'test_body',
                                 data.read(),
                                 'test.jpg')
        data.close()
        attach_file = None
        attach_file_name = ''
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
            if part.get_filename():
                attach_file = part.get_payload(decode=True)
                attach_file_name = part.get_filename()
        self.assertEqual(body, b'test_body')
        data = open('tests/test.jpg', 'rb')
        self.assertEqual(attach_file, data.read())
        data.close()
        self.assertEqual(attach_file_name, 'test.jpg')

    @mock_ses
    def test_send_mail(self):
        ses = boto3.client('ses', region_name='us-east-1')
        ses.verify_email_identity(EmailAddress='test@example.com')
        data = open('tests/test.jpg', 'rb')
        attach_file = data.read()
        attach_file_name = 'test.jpg'
        data.close()
        msg = aws_util.make_mime('test@example.com',
                                 'test_subject',
                                 'test_body',
                                 attach_file,
                                 attach_file_name)
        responses = aws_util.send_email(ses,
                                        'test@example.com',
                                        'test_to@example.com',
                                        msg)
        self.assertEqual(responses[0]['ResponseMetadata']['HTTPStatusCode'], 200)


if __name__ == "__main__":
    unittest.main()