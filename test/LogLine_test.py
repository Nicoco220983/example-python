#!/usr/bin/env python3
import unittest
from LogLine import LogLine
import datetime

log_line_str = '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123'

class LogLineTest(unittest.TestCase):

  def test_ok(self):

    # parse a log line
    logLine = LogLine(log_line_str)   

    # check all attriutes
    self.assertEqual(logLine.remotehost, '127.0.0.1')
    self.assertEqual(logLine.rfc931, None)
    self.assertEqual(logLine.authuser, 'james')
    self.assertEqual(logLine.date, datetime.datetime(2018, 5, 9, 16, 0, 39, tzinfo=datetime.timezone.utc))
    self.assertEqual(logLine.request, 'GET /report HTTP/1.0')
    self.assertEqual(logLine.status, 200)
    self.assertEqual(logLine.bytes, 123)

    self.assertEqual(logLine.method, 'GET')
    self.assertEqual(logLine.resource, '/report')
    self.assertEqual(logLine.version, 'HTTP/1.0')
    self.assertEqual(logLine.section, 'report')

