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
#Setup Email header since the script logs to a file.
print("From: mailer <mail@mail.com> ")
print("To: mail@mail.com") 
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
for file in os.listdir(NEW_DIR):
    if file.startswith("p"):
     config_path = os.path.join(NEW_DIR, file)
     parse = CiscoConfParse(config_path)
     all_intfs = parse.find_objects(r"^interf")
     NoDot1x = list()
     NoDot1x = parse.find_objects_wo_child(r'^interface', r'authentication')
     #Remove Non Gig Ports because all user ports are 1 gig
     GigPorts = [x.text.split()[1] for x in NoDot1x if x.text.startswith("interface Gig")]
     #Remove Cisco 3750 Exansion module
     final_list=[w for w in GigPorts if not re.match(r'GigabitEthernet./1/.', w)]
     #Netmiko Gets Port Descriptions
     for t in final_list:
        port= ''.join(t)
        if port.startswith('GigabitEthernet'):
           cmd = 'show run int {0} | i desc' .format(port)
           net_connect = ConnectHandler(device_type='cisco_ios', host=file, username='changeme', password='changeme') 
           desc = net_connect.send_command(cmd)
           result = file +'   ' + ''.join(port)+ "   " + desc
           print(result)
        else:
           result = file + "All user ports have 802.1x enabled"
           print (result)
#print("-------------------The script has finished------------------------")
