import logging
import os
import json 

# Have to put file check here so it can import
class f_check:
    def __init__(self):
        f_path = os.path.join(os.path.dirname(__file__), 'conf', 'config.json')
        with open(f_path, 'r') as json_file:
            self.loaded = json.load(json_file)

f = f_check()
try:
    level = logging.getLevelName(f.loaded['tenants'][0]['debug_level'])
except:
    logging.basicConfig(level = logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S', \
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s')
else:
    logging.basicConfig(level = level, datefmt='%Y-%m-%d %H:%M:%S', \
        format='%(asctime)s %(name)s %(levelname)-8s %(message)s')
