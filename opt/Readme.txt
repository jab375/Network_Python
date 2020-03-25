The following scripts check for missing or excessive configurations on Cisco IOS devices.


How to use Findmissing.py
Below is part of the code from Findmissing.py and it objective is to look for the SNMP read configurations in cisco syntax and if it is 
missing Python will print out the results in the CLI screen. To edit what the script looks for, the funvar variable will need to be change 
to match what syntax in the configuration file you are looking for. If theere is a simlar syntax, you can add a comma and add another 
syntax to look for example would be if the managment ACL is named differntly. funvar=["snmp-server community READCOM RO mgmtacl","snmp-
server community READCOM RO aclmgmt" ]


    for host in os.listdir(dir):
       #Define where configs are stored
       config_path = os.path.join(dir, host)
       #Check for SNMP Read
       funvar=["snmp-server community READCOM RO mgmtacl"]
