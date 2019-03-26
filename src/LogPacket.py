from LogLine import LogLine
import datetime

# a LogPacket gathers all the LogLine of a given period
class LogPacket:

  # constructor
  def __init__(self, log_lines, period):
    # input attributes
    self.init_log_lines(log_lines)
    self.period = period
    # requets per second
    self.rps = len(self.log_lines) / self.period
    # (sorted) requests per sections
    self.section_group = self.group_log_lines_by("section")
    # (sorted) requests per status
    self.status_group = self.group_log_lines_by("status")
    # requests per authuser
    self.authuser_group = self.group_log_lines_by("authuser")

  # init log lines by parsing them
  def init_log_lines(self, log_lines):
    self.log_lines = []
    self.nb_invalid_log_lines = 0
    # split lines, and get ride of empty ones
    lines = filter(None, log_lines.split('\n'))
    # for each line, try to parse it into a LogLine
    # the try/catch allow to be resilient to any log file error
    for l in lines:
      try:
        self.log_lines.append(LogLine(l))
      except:
        self.nb_invalid_log_lines += 1

  # group LogLine by a given attribute
  def group_log_lines_by(self, attr):
    # build a dictionary of key -> nb log lines
    res_dict = {}
    for ll in self.log_lines:
      key = getattr(ll, attr)
      if key is None: continue
      res_dict[key] = res_dict.get(key, 0) + 1
    # convert it to array, and sort it (from higher to lower)
    res_arr = [(key, nb) for key, nb in res_dict.items()]
    return list(sorted(res_arr, key = lambda e: e[1], reverse = True))

  # method to print a LogPacket
  def __repr__(self):
    res = ""
    # format log packet
    nb_log_lines = len(self.log_lines)
    res = (
      "[{date}]\n"
      "Log monitoring of last {period} seconds:\n"
      "- Number of HTTP requests: {nb}\n"
    ).format(
      date = datetime.datetime.now(),
      period = self.period,
      nb = nb_log_lines
    )
    # following infos will be showed only if there is at least 1 log in the period
    if nb_log_lines > 0:
      res += (
        "- Average requests per second: {rps}\n"
        "- Average size of requests: {size} bytes\n"
      ).format(
        rps = self.rps,
        size = round( sum([ll.bytes for ll in self.log_lines]) / nb_log_lines )
      )
    # auth users
    nb_authuser = len(self.authuser_group)
    if nb_authuser > 0:
      avg_requests_by_authuser = sum([nb for (_, nb) in self.authuser_group]) / nb_authuser
      res += (
        "- Average number of requests by authentified users: {avg}\n"
      ).format(
        avg = round(avg_requests_by_authuser, 1)
      )
    # format most requested sections
    res += self.repr_log_lines_group(
      "Most requested sections",
      self.section_group,
      5)
    # format response status
    res += self.repr_log_lines_group(
      "Reponse statuses",
      self.status_group,
      5)
    # check if there are invalid log lines
    if self.nb_invalid_log_lines > 0:
      res += (
        "[WARNING] Number of invalid HTTP requests: {nb_invalid}\n"
      ).format(
        nb_invalid = self.nb_invalid_log_lines
      )
    return res

  # format any log line group
  def repr_log_lines_group(self, title, group, limit):
    # check if there is at least log line
    res, nb_log_lines = "", len(self.log_lines)
    if nb_log_lines > 0:
      # add title
      res += title + ' :\n'
      # only show "limit" highest values
      for i in range(min(limit, len(group))):
        key, nb = group[i] 
        res += "- {key}: {percentage}%\n".format(
          key = key,
          percentage = round(nb / nb_log_lines * 100)
        )
    return res
