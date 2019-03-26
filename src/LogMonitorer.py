#!/usr/bin/env python3

import time, datetime
from math import ceil
from optparse import OptionParser
from LogPacket import LogPacket

# default input values
default_log_file_path = "/tmp/access.log"
default_period = 10
default_high_traffic_threshold = 10
default_high_traffic_duration = 120

# main function (in case LogMonitorer is called as a script)
def main():
  # parse input options
  parser = OptionParser()
  parser.add_option(
    "-f", "--file",
    type = "string",
    default = default_log_file_path,
    help = "Path to log file to monitor [default: %default]")
  parser.add_option(
    "-p", "--period",
    type = "int",
    default = default_period,
    help = "Period on which monitorer will print a summary of logs "
           "[unit: seconds] [default: %default]")
  parser.add_option(
    "-t", "--high_traffic_threshold",
    type = "int",
    default = default_high_traffic_threshold,
    help = "Traffic threshold above which monitorer will print a warning "
           "[unit:request per second] [default: %default]")
  parser.add_option(
    "-d", "--high_traffic_duration",
    type = "int",
    default = default_high_traffic_duration,
    help = "Duration above which high traffic warning is printed "
           "[unit: seconds] [default: %default]")
  (options, args) = parser.parse_args()
  # call monitorer
  LogMonitorer(
    log_file_path = options.file,
    period = options.period,
    high_traffic_threshold = options.high_traffic_threshold,
    high_traffic_duration = options.high_traffic_duration)
  
# class to monitor a W3C log file
class LogMonitorer:

  # constructor
  def __init__(self,
               log_file_path = default_log_file_path,
               period = default_period,
               high_traffic_threshold = default_high_traffic_threshold,
               high_traffic_duration = default_high_traffic_duration):
    # input attributes
    self.log_file_path = log_file_path
    self.period = period
    self.high_traffic_threshold = high_traffic_threshold
    self.high_traffic_duration = high_traffic_duration
    # other attributes
    self.log_packets = []
    self.log_file = None
    self.high_traffic = False
    # start monitoring
    self.start()

  # destructor
  def __del__(self):
    # release log file resource
    self.close_log_file()

  # start monitoring loop
  def start(self):
    # open log file
    self.open_log_file()
    # start monitor loop
    self.start_monitor_loop()

  def start_monitor_loop(self):
    # monitoring loop
    while True:
      try:
        time.sleep(self.period)
        self.monitor_iteration()
      except KeyboardInterrupt:
        # do not print ugly stack at monitorer interruption
        return
      except Exception as e:
        # else just print error, and continue
        self.log("[ERROR] {}".format(e))

  # open log file
  def open_log_file(self):
    self.log_file = open(self.log_file_path, 'r')
    # go directly to the end of file
    self.log_file.seek(0, 2)

  # close log file (only if opened)
  def close_log_file(self):
    if self.log_file is not None:
      self.log_file.close()
      self.log_file = None

  # monitor loop iteration
  def monitor_iteration(self):
    # read new logs
    logs = self.read_log_file()
    # convert them to LoPacket
    log_packet = LogPacket(logs, self.period)
    self.log_packets.append(log_packet)
    # log info about about log_packet
    self.log(log_packet)
    # check high traffic
    self.check_high_traffic()

  # check for high traffic
  def check_high_traffic(self):
    # check if there is enough log packets to compute average TPS
    nb_packets_to_check = ceil(self.high_traffic_duration / self.period)
    if(len(self.log_packets) < nb_packets_to_check): return
    # compute average TPS on last "nb_packets_to_check" LogPackets
    sum_rps = sum([p.rps for p in self.log_packets[-nb_packets_to_check:]])
    avg_rps = sum_rps / nb_packets_to_check
    # compare average TPS to threshold
    if avg_rps >= self.high_traffic_threshold:
      if not self.high_traffic:
        self.high_traffic = True
        self.log_start_high_traffic(avg_rps)
    else:
      if self.high_traffic:
        self.high_traffic = False
        self.log_end_high_traffic()

  # log high traffic alert
  def log_start_high_traffic(self, avg_rps):
    self.log((
      "[WARNING] High traffic generated an alert - "
      "hits = {avg_rps} requests per second, triggered at {time}\n"
    ).format(
      avg_rps = avg_rps,
      time = datetime.datetime.now()
    ))

  # log end of high traffic alert
  def log_end_high_traffic(self):
    self.log("[WARNING] End of high traffic alert\n")

  # small methods that can easily been overwritten in a test case

  def read_log_file(self):
    return self.log_file.read()

  def log(self, s):
    print(s)


if __name__ == "__main__":
  main()
