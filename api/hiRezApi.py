from datetime import datetime, timedelta
from hashlib import md5
import json
import os

import requests


class HiRezAPI:


    def __init__(self, endpoint, save_session = True):

        with open("api/api.json", "r") as f:
            api_data = json.load(f)

        self.name_cls = self.__class__.__name__
        self.dev_id = api_data["HiRez"][0]["dev_id"]
        self.auth_key = api_data["HiRez"][0]["auth_key"]
        self.endpoint = endpoint
        self.headers = {}
        self.save_session = save_session
        self.session = self.session_to_json('r')
        


    def sign(self, api_method):

        signature = f'{self.dev_id}{api_method.lower()}{self.auth_key}{self.timestamp()}'

        return md5(signature.encode("utf-8")).hexdigest()
    

    def get_session(self):

        if datetime.utcnow() - self.session['time'] > timedelta(minutes=14, seconds=59):

            self.session['id'] = self.create_session()

            if self.save_session:
                self.session_to_json('w')
                self.test_session()

        return self.session['id']
    

    def request(self, url, *args, **kwargs):

        r = requests.get(url=url, headers={**self.headers, **kwargs.pop('headers', {})}, *args, **kwargs)
        if r.headers.get('Content-Type', '').rfind('json') != -1:
            return r.json()

        return r.text
    

    def timestamp(self):

        return datetime.utcnow().strftime('%Y%m%d%H%M%S')


    def create_url(self, api_method, *args):

        url = f'{self.endpoint}{api_method}json/{self.dev_id}/{self.sign(api_method)}/{self.get_session()}/{self.timestamp()}'

        for arg in args:
            url += str(f'/{arg}')

        return url
    

    def session_to_json(self, method):

        if method == 'r' or method == 'read':
            if self.save_session:
                if os.path.isfile('api/session_data.json'):
                    with open('api/session_data.json', "r") as read_file:
                        data_json = json.load(read_file)
                    if self.__class__.__name__ in data_json:
                        self.session = data_json[self.__class__.__name__]
                        self.session['time'] = datetime.strptime(self.session['time'], "%Y-%m-%d %H:%M:%S.%f")
                        return self.session

            self.session = {'id': None,
                            'time': datetime.utcnow() - timedelta(minutes=15)}

            return self.session

        if method == 'w' or method == 'write':
            if os.path.isfile('api/session_data.json'):
                with open('api/session_data.json', "r") as read_file:
                    data_json = json.load(read_file)
                data_json[self.name_cls] = self.session
                with open('api/session_data.json', "w") as write_file:
                    json.dump(data_json, write_file, default=str, indent=4)
            else:
                with open('api/session_data.json', "w") as write_file:
                    json.dump(({self.name_cls: self.session}), write_file, default=str, indent=4)


    # Connectivity, Development, & System Status


    def ping(self):

        return self.request('f{self.endpoint}/pingjson')
    

    def create_session(self):

        sign = self.sign("createsession")
        url_session = f'{self.endpoint}{"createsession"}json/{self.dev_id}/{sign}/{self.timestamp()}'
        self.session['time'] = datetime.utcnow()

        response = self.request(url_session)

        if response.get('ret_msg', '').lower() == 'approved':

            return response.get('session_id')
        
        return 0
    

    def test_session(self):

        return self.request(self.create_url('testsession'))
    

    def data_used(self):

        return self.request(self.create_url('getdataused'))
    

    def server_status(self):

        return self.request(self.create_url('gethirezserverstatus'))
    

    def patch_info(self):

        return self.request(self.create_url('getpatchinfo'))
