import re
from datetime import datetime

# regex to parse a log line
logline_regex = (
  '({word})'
  '{space}'
  '({word})'
  '{space}'
  '({word})'
  '{space}'
  '\[({all})\]'
  '{space}'
  '"({all})"'
  '{space}'
  '({number})'
  '{space}'
  '({number})'
).format(
  word = '[\w.:/-]+',
  number = '\d+',
  space = '\s+',
  all = '.+'
)

# class to parse a W3C log line
class LogLine:

  # set W3C log line fields
  remotehost = None
  rfc931 = None
  authuser = None
  date = None
  request = None
  status = None
  bytes = None

  # other computed attriutes
  method = None
  resource = None
  version = None

  section = None

  # constructor
  def __init__(self, line):

    # parse input string log line
    attrs = self.parse_log_line(line)

    # set W3C log line attributes
    self.remotehost = attrs[0]
    self.rfc931 = attrs[1] if attrs[1] != '-' else None
    self.authuser = attrs[2] if attrs[2] != '-' else None
    self.date = datetime.strptime(attrs[3], '%d/%b/%Y:%H:%M:%S %z')
    self.request = attrs[4]
    self.status = int(attrs[5])
    self.bytes = int(attrs[6])

    # compute other attributes
    self.method, self.resource, self.version = self.request.split()
    self.init_section()

  def init_section(self):
    resource_split = self.resource.split('/')
    # remove empty strings (caused by leading '/' )
    resource_split = filter(None, resource_split)
    # set first split as section
    self.section = next(resource_split, '')

  # parse W3C log line, and create LogLine from it
  def parse_log_line(self, line):
    m = re.match(logline_regex, line)
    return m.groups()

