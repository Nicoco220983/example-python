#!/usr/bin/env python3
import unittest
from LogPacket import LogPacket

log_line_str = '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123'
invalid_log_line_str = 'invalid'

# build 10 concatenated log lines
log_packet_str = ""
for i in range(10):
  log_packet_str += log_line_str + '\n'
log_packet_str += invalid_log_line_str + '\n'

class LogPacketTest(unittest.TestCase):

  def test_ok(self):

    # parse log lines
    log_packet = LogPacket(log_packet_str, 10)   

    # check all attributes
    self.assertEqual(len(log_packet.log_lines), 10)
    self.assertEqual(log_packet.rps, 1)
    self.assertEqual(log_packet.nb_invalid_log_lines, 1)
    self.assertEqual(log_packet.section_group[0], ("report", 10))
    self.assertEqual(log_packet.status_group[0], (200, 10))

