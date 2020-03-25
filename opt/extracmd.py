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
def config_check_extra():
      if host.endswith("Switch01") or host.endswith("Switch04"):
      #Ignore These Devices by setting p to equal 0
         p=0
      else:
         for y in findme:
             for line in open(config_path).readlines():
                 if line.startswith(y):
                    ingoreme="false"
                    for x in ignore:
                        if x in line:
                           ingoreme= "true"
                    for x in ignore:
                       #print("Evaluating     ",line, "Should I Ignore    ", ingoreme)
                        if x in line:
                           p=0
                        elif ingoreme == "false":
                             print(host,"   Extra   ", line)
                             break

#Check for Extra NTP Commands
for host in os.listdir(dir):
    #Define where configs are store
    config_path = os.path.join(dir, host)
    ignore=["ntp server 1.5.12.2 prefer", "ntp server vrf Mgmt-intf 1.5.12.2 prefer","ntp server 1.5.12.3",
            "ntp server vrf Mgmt-intf 10.59.128.3", "ntp source", "clock-period",
            "clock timezone EST -5","clock timezone EST -5 0","clock summer-time EDT recurring",
            "service timestamps log datetime msec localtime show-timezone",
            "service timestamps debug datetime msec localtime show-timezone"]
    findme=["ntp","clock","service time"]
    config_check_extra()
