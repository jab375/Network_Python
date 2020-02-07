#
#Int Modules
#
import os
import re
import pathlib
#Define variables
snmpread="snmp-server community readcommunity RO 98"
snmpwrite="snmp-server community writecommunity RW 98"
ace1="access-list 98 remark -- SNMP Access"
ace2="access-list 98 permit 1.1.1.1"
ace3="access-list 98 permit 2.2.2.2"
ace4="access-list 98 permit 3.3.3.3"
ace5="access-list 98 permit 4.4.4.4"
ace6="access-list 98 permit 5.5.5.5"
ignore1="snmp-server location"
ignore2="snmp-server contact"
#Start Examining configs for Missing SNMP configurations
header = "The following have bad NTP configurations"
print(header)
dir = "/opt/modconfigs"
for host in os.listdir(dir):
    config_path = os.path.join(dir, host)
#SNMP READ
    found = False
    for line in open(config_path).readlines():
      if snmpread in line:
         found = True
         break
    if found is False:
       print(host, " is missing SNMP read community :", snmpread)
#SNMP WRITE
    found = False
    for line in open(config_path).readlines():
      if snmpwrite in line:
         found = True
         break
    if found is False:
       print(host, " is missing SNMP write community :", snmpwrite)
       
#Find Excessive SNMP
header = "The following have too many SNMP configurations"
print(header)
dir = "/opt/modconfigs"
for host in os.listdir(dir):
    config_path = os.path.join(dir, host)
    for line in open(config_path).readlines():
        p=0
        if line.startswith(snmpread) or line.startswith(snmpwrite) or line.startswith(ignore1) or line.startswith(ignore2):
        #Ignore these snmp settings
           p=1
        elif line.startswith("snmp") and p is 0:
           print(host,"has extra SNMP command", line)

#Find Excessive SNMP ACE
header = "The following have too many SNMP ACL configurations"
print(header)
dir = "/opt/modconfigs"
for host in os.listdir(dir):
    config_path = os.path.join(dir, host)
    for line in open(config_path).readlines():
        p=0
        if line.startswith(ace1) or line.startswith(ace2) or line.startswith(ace3) or line.startswith(ace4) or line.startswith(ace5) or line.startswith(ace6):
           #Ignore these snmp settings
           p=1
        elif line.startswith("access-list 98") and p is 0:
           print(host,"has extra SNMP ACE command", line)

