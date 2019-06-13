#
#Int Modules
#
import os
import re
import shutil
import pathlib
from ciscoconfparse import CiscoConfParse
from netmiko import ConnectHandler
#
#Setup Email header since the script logs to a file because of ansible.
print("From: SGP-NETDB <NetDB@SafeguardProperties.com> ")
print("To: NetTeam@safeguardproperties.com") 
print("Subject: Ports Without 802.1x") 
#
# Rename OLD_DIR Files and move them to the NEW_DIR location
#
#print("-------------------Starting to remove -Running.config from file name-----------------")
OLD_DIR = '//home/zjabn3tw/Nodot1x/Configs'
NEW_DIR = '/home/zjabn3tw/Nodot1x/modifiedconfigs'
p = pathlib.Path(OLD_DIR)
for f in p.glob('**/*-Running.Config'):
    #new_name = '{}_{}'.format(f.parent.name, f.name)     
    new_name = '{}'.format(f.parent.name,f.name)
    f.rename(os.path.join(NEW_DIR, new_name))
#print(" ")
#print("-------------------Finshed removing -Running.config from file name-------------------")
#print(" ")
header = "Switch"+ "        " + "Port W/O Dot1x" +"          "+ "Port Description"
print(header)
#
#Start Examining configs for missing port security
#
for host in os.listdir(NEW_DIR):
    if host.startswith("p"):
     config_path = os.path.join(NEW_DIR, host)
     parse = CiscoConfParse(config_path)
     all_intfs = parse.find_objects(r"^interf")
     NoDot1x = list()
     NoDot1x = parse.find_objects_wo_child(r'^interface', r'authentication')
     #Remove Non Gig Ports because all user ports are 1 gig
     GigPorts = [x.text.split()[1] for x in NoDot1x if x.text.startswith("interface Gig")]
     #Remove Cisco 3750 Exansion module
     final_list=[w for w in GigPorts if not re.match(r'GigabitEthernet./1/.', w)]
     #Gets Port Descriptions
     for ports in final_list:
         port = "interface" + " " + ports
         intconfig = parse.find_children(port, exactmatch=True)
         desc = [x for x in intconfig if re.search("description", x)]
         result = host+'   ' + ''.join(ports)+'   '+ ''.join(desc)   
         print(result)
