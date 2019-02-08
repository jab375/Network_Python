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
# Rename OLD_DIR Files and move them to the NEW_DIR location
#
print("-------------------Starting to remove -Running.config from file name-----------------")
OLD_DIR = '//home/jbowers/removevlan/configs'
NEW_DIR = '/home/jbowers/removevlan/modifiedconfigs'
p = pathlib.Path(OLD_DIR)
for f in p.glob('**/*-Running.Config'):
    #new_name = '{}_{}'.format(f.parent.name, f.name)     
    new_name = '{}'.format(f.parent.name,f.name)
    f.rename(os.path.join(NEW_DIR, new_name))
print("-------------------Finshed removing -Running.config from file name--------------------")
print("-------------------Starting to Remove Vlan--------------------------------------------") 
#
#Start Examining configs for missing port security
#
for file in os.listdir(NEW_DIR):
    if not file.startswith("P"):
        continue
    config_path = os.path.join(NEW_DIR, file)
    parse = CiscoConfParse(config_path)
    all_intfs = parse.find_objects(r"^interf")
    intchange = list()
    #
    #intchange Variable finds all ports on Vlanxxx. This is the vlan you want to remove
    #
    intchange = parse.find_objects_w_child(r'^interface', r'switchport access vlan 543')
    gigports = [x.text.split()[1] for x in intchange if x.text.startswith("interface Gig")]
    final_list=[w for w in gigports if not re.match(r'GigabitEthernet./1/.', w)]
    #Netmiko Gets Port Descriptions
    for t in final_list:
       port= ''.join(t)
       if port.startswith('GigabitEthernet'):
          cmd1 = 'configure term'
          cmd2 = 'int {0}' .format(port)
          #
          #cmd3 needs to be configured to the new vlan you want on the ports
          #
          cmd3 = 'switchport access vlan 414'
          cmd4 = 'exit'
          net_connect = ConnectHandler(device_type='cisco_ios', host=file, username='   ', password='    ')
       
          config_commands = [cmd2,cmd3]
          output = net_connect.send_config_set(config_commands)
          print(output)
          net_connect.disconnect()
       else:
          result = file + "Has no ports on the vlan wanting to be removed"
          print (result)
print("-------------------The script has finished------------------------")

