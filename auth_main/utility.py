import csv
import os
import json
from datetime import datetime
from .logger import logging as log
from .logger import f_check
from cachetools import TTLCache
import traceback
import getpass
import requests
# Check for DMC and if not installed, let user know and continue
try:
    from dmc import gettoken
except ImportError:
    log.warning("Please use pip install centrify.dmc to use DMC auth")

f = f_check()

# For the OAUTH process

class auth:
    def __init__(self, password, **kwargs):
        if kwargs['auth'].upper() == 'DMC':
            log.info('Setting auth headers for DMC......')
            self._headers = {}
            self._headers["X-CENTRIFY-NATIVE-CLIENT"] = 'true'
            self._headers['X-CFY-SRC' ]= 'python'
            try:
                self._headers['Authorization']  = 'Bearer {scope}'.format(**kwargs)
            except KeyError:
                log.error('Issue with getting DMC scope')
                raise Exception
        elif kwargs['auth'].upper() == 'OAUTH':
            log.info("Going to authenticate Oauth account: {client_id}".format(**kwargs['body'])) 
            # Handle the fact that client_secret can be added to the config file and skip the ask
            self.json_d = json.dumps(kwargs['body'])
            self.update = json.loads(self.json_d)
            self.update['scope'] = kwargs['scope']
            self.update['client_secret'] = password
            self._rheaders = {}
            self._rheaders['X-CENTRIFY-NATIVE-CLIENT'] = 'true'
            self._rheaders['Content-Type'] = 'application/x-www-form-urlencoded'
            log.info('Oauth URL of app is: {tenant}/Oauth2/Token/{appid}'.format(**kwargs, **kwargs['body'])) 
            log.info('Oauth token request Headers are: {}'.format(self._rheaders)) 
            try:
                log.info('Setting auth headers for OAUTH......')
                req = requests.post(url='{tenant}/Oauth2/Token/{appid}'.format(**kwargs, **kwargs['body']), headers= self._rheaders, data= self.update).json()
            except:
                log.error("Issue getting token")
                log.error("Response: {0}".format(json.dumps(req)))
            self._headers = {}
            self._headers["Authorization"] = "Bearer {access_token}".format(**req)
            self._headers["X-CENTRIFY-NATIVE-CLIENT"] = 'true'
        else:
            log.error("Not valid auth type. Please fix")
    @property
    def headers(self):
        return self._headers

# Cache class that utilizes the auth class

class Cache:
    def __init__(self, password, **kwargs):
        # Make TTL setting to grab in conf file next to debug
        self._cache = TTLCache(maxsize=10, ttl=600)
        try:
            log.info("Building the cache..")
            self._cache['header'] = auth(password, **kwargs).headers
            self._cache['tenant'] = kwargs['tenant']
        except Exception as e:
            log.error("Failed to build cache")
            log.error(traceback.print_exc(e))
            raise SystemExit(0)
    @property
    def ten_info(self):
        return self._cache
    @property
    def dump(self):
        log.info("Dumping the cache.")
        self._cache.clear()