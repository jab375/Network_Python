#
#Int Modules
#
import os
import re
import pathlib
#print("-------------------Starting to remove -Running.config from file name-----------------")
OLD_DIR = '//opt/configs'
NEW_DIR = '/opt/modconfigs'
p = pathlib.Path(OLD_DIR)
for f in p.glob('**/*-Running.Config'):
    new_name = '{}'.format(f.parent.name,f.name)
    f.rename(os.path.join(NEW_DIR, new_name))
#print(" ")
#print("-------------------Finshed removing -Running.config from file name-------------------")
#print(" ")
