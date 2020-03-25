#
#Int Modules
#
import os
import re
import pathlib
#Define variables and print header
header = "The following have bad configurations"
print(header)
dir = "/opt/scripts/modconfigs"
####Functions
def config_check_missing():
   if host.endswith("switch01") or host.endswith("Switch04"):
      #Ignore These Devices by setting p to equal 0
      p=0
   else:
      found = False
      for x in funvar:
          for line in open(config_path).readlines():
              if x in line:
                 found = True
      #If Funvar is not found then report the missing
      if found is False:
          printme = ""
          printme += host
          printme += " is missing "
          counter = 0
          for x in funvar:
              if counter < 1:
                 printme += x
                 counter += 1
              else:
                 printme += " or "
                 printme += x
          print(printme)

#Begin Checks by looping through the modconfigs directory
#NTP/Clock/Service Related Checks
for host in os.listdir(dir):
    #Define where configs are stored
    config_path = os.path.join(dir, host)
    #Check for Primary NTP Server
    funvar=["ntp server 10.5.12.2 prefer", "ntp server vrf Mgmt-intf 10.5.18.2 prefer"]
    config_check_missing()
    #Check for Secondary NTP Server
    funvar=["ntp server 10.5.12.3", "ntp server vrf Mgmt-intf 10.5.18.3"]
    config_check_missing()
    #Check for time stamp logs
    funvar=["service timestamps debug datetime msec localtime show-timezone"]
    config_check_missing()
    funvar=["service timestamps log datetime msec localtime show-timezone"]
    config_check_missing()
    #Check for Service Encryption
    funvar=["service password-encryption"]
    config_check_missing()
    #Check for EST Timezone is set
    funvar=["clock timezone EST -5","clock timezone EST -5 0"]
    config_check_missing()
    funvar=["clock summer-time EDT recurring"]
    config_check_missing()

#SNMP Related Checks
for host in os.listdir(dir):
    #Define where configs are stored
    config_path = os.path.join(dir, host)
    #Check for SNMP Read
    funvar=["snmp-server community ReadCom RO mgmtacl"]
    config_check_missing()
    #Check for SNMP Write
    funvar=["snmp-server community WriteCom RW mgmtacl"]
    config_check_missing()
    #Check for SNMP ACL. Cisco oldway + New way with ACE placement
    funvar= ["ip access-list standard mgmtacl", "10 remark -- SNMP Access"]
    config_check_missing()
