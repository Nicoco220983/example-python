#!/usr/bin/env python3
import unittest
from LogMonitorer import LogMonitorer
from os import remove
from os.path import dirname, join


# TEST FILE ######################

# compute test file path
here = dirname(__file__)
test_file_path = join(here, '_test_access.log')

# function to append some content to test file
def fill_test_file(content):
  with open(test_file_path, 'a') as file:
    file.write(content)


# LOG LINES ######################

# test log line
log_line_str = '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123'
# function to concatenate several log lines
def build_log_packet(nb_lines):
  res = ""
  for i in range(nb_lines):
    res += log_line_str + '\n'
  return res


# MOCK ######################

# LogMonitorer mocked for testing
class LogMonitorerMock(LogMonitorer):

  # constructor
  def __init__(self, **kwargs):
    # set log file path to test file
    kwargs["log_file_path"] = test_file_path
    # parent constructor
    LogMonitorer.__init__(self, **kwargs)
    # additional attributes
    self.test_monitor_logs = []

  # do not start infinite loop, instead monitor method will be manually called in tests
  def start_monitor_loop(self):
    pass

  # fill self.test_monitor_logs instead of printing
  def log(self, s):
    self.test_monitor_logs.append(s)


# TESTS ######################

class LogMonitorTest(unittest.TestCase):

  # called at each beginning of test
  def setUp(self):
    # create empty test file
    open(test_file_path, 'w').close()
    # create log monitorer
    self.log_monitorer = LogMonitorerMock()
    

  # called at each end of test
  def tearDown(self):
    # release resource on file
    self.log_monitorer.close_log_file()
    # remove test file
    remove(test_file_path)

  # basic test
  def test_ok(self):

    # inject 10 logs
    fill_test_file(build_log_packet(10))
    self.log_monitorer.monitor_iteration()

    # check that monitorer worked
    self.assertEqual(len(self.log_monitorer.test_monitor_logs), 1)

  # test high traffic alert
  def test_high_traffic(self):

    # inject 10 RPS during 12 iteration (120 seconds)
    for i in range(12):
      fill_test_file(build_log_packet(100))
      self.log_monitorer.monitor_iteration()

    # check that alert has been triggered
    self.assertEqual(len(self.log_monitorer.test_monitor_logs), 13)
    self.assertTrue("High traffic generated an alert - hits = 10.0 requests per second" in self.log_monitorer.test_monitor_logs[-1])

    # inject few message during one iteration
    fill_test_file(build_log_packet(1))
    self.log_monitorer.monitor_iteration()
    # check that end of alert has been triggered
    self.assertTrue("End of high traffic alert" in self.log_monitorer.test_monitor_logs[-1])


