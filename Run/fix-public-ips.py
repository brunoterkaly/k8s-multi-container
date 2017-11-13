
import subprocess
from shutil import copyfile
import re
import sys
import time
import socket
import datetime

def extract_line(s):
  s = re.sub('\x1b[^m]*m', '', s)
  s = re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', s)
  sep = re.compile('[\s]+')
  #addToTopFile(s)
  s = sep.split(s)
  #del s[-1]
  return s[3]



def skipLinesUntilToken(process, token):
    i = 0
    for line in process.stdout:
       s = line.decode('utf-8')
       i += 1
       if s.find(token) != -1:
         break;
    return s

def getExternalIp():
    try:
       while True:
           last_read_good = 0
           command = ['kubectl', 'get', 'svc']
           process = subprocess.Popen(command, stdout=subprocess.PIPE)
           s = skipLinesUntilToken(process,"web1")
           #print(s)
           result = extract_line(s)
           process.terminate()
           return result
    except KeyboardInterrupt:
       pass
    return

IP_MATCHER = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
def extract_proxies(fh):
    buffer = []
    for line in fh:
        line = line.strip()
        match = IP_MATCHER.findall(line)
        if match:
            buffer.append(match)
        else:
            pass
    return buffer

def do_fix(fn, newip):
   iplist = extract_proxies(open(fn))
   #print(iplist)
   #print(iplist[1][0])
   for i in range(len(iplist)):
       with open(fn) as f:
            s = f.read()
            s = s.replace(iplist[i][0], newip)
       with open(fn, "w") as f:
            f.write(s)

# Get new IP
newip = getExternalIp()
print("public ip address for web service = ",newip)
do_fix("init.sh", newip)
do_fix("add.sh", newip)
do_fix("query.sh", newip)


