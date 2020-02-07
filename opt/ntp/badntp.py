#
#Int Modules
#
import os
import re
import pathlib

#Define variables
ntpserver1="ntp server 1.1.1.1 prefer"
ntpserver2="ntp server 2.2.2.2"
ntpserver3="ntp server vrf Mgmt-intf 1.1.1.1 prefer"
ntpserver4="ntp server vrf Mgmt-intf 2.2.2.2"
ntpservice1="service timestamps debug datetime msec localtime show-timezone"
ntpservice2="service timestamps log datetime msec localtime show-timezone"
timezone1="clock timezone EST -5"
timezone2="clock timezone EST -5 0"
daylight1="clock summer-time EDT recurring"
daylight2="clock summer-time EDT 2 Sun Mar 2:00 1 Sun Nov 2:00 60"
ntpsource="ntp source"
ntpperiod="ntp clock-period"

#Start Examining configs for Missing NTP configurations
header = "The following have bad NTP configurations"
print(header)
dir = "/opt/modconfigs"
for host in os.listdir(dir):
    config_path = os.path.join(dir, host)
# If statment will ignore Core Switches since these are NTP servers
    if host.endswith("coreswith1") or host.endswith("coreswith2"):
      p=0
    else:
#NTP Server
      found = False
      for line in open(config_path).readlines():
        if ntpserver1 in line or ntpserver3 in line :
          found = True
          break
      if found is False:
         print(host, " is missing NTP :", ntpserver1)

#NTP Server
      found = False
      for line in open(config_path).readlines():
        if ntpserver2 in line or ntpserver4 in line :
          found = True
          break
      if found is False:
         print(host, " is missing NTP :", ntpserver2)

#Check NTP service commands
      found = False
      for line in open(config_path).readlines():
        if ntpservice1 in line or ntpservice2 in line:
          found = True
          break
      if found is False:
         print(host, " is missing NTP :", ntpservice1, "or", ntpservice2)

#Check Timezone
      found = False
      for line in open(config_path).readlines():
        if timezone1 in line or timezone2 in line:
          found = True
          break
      if found is False:
         print(host, " is missing NTP :", timezone2)

#Check Daylight
      found = False
      for line in open(config_path).readlines():
        if daylight1 in line or daylight2 in line:
          found = True
          break
      if found is False:
         print(host, " is missing NTP :", daylight1)

#Find extra Syslog configurations
header = "The following have too many NTP configurations"
print(header)
dir = "/opt/modconfigs"
for host in os.listdir(dir):
    # If statment will ignore Core Switches since these are NTP servers
    if host.endswith("coreswith1") or host.endswith("coreswith2"):
      p=0
    else:
      config_path = os.path.join(dir, host)
      for line in open(config_path).readlines():
          p=0
          if line.startswith(ntpserver1) or line.startswith(ntpserver2) or line.startswith(ntpserver3) or line.startswith(ntpserver4):
             #Ignore NTP Server
             p=1
          if line.startswith(ntpsource) or line.startswith(ntpperiod):
            #Another Ignore
             p=1
          elif line.startswith("ntp") and p is 0:
             print(host,"has extra NTP command", line)
