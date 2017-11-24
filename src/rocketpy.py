#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Simple wrapper of Rocket.Chat API.
'''

from http.client import HTTPConnection, HTTPSConnection, HTTPException
from http import HTTPStatus
from urllib.parse import urlparse
import json


class REST:
    '''Simple wrapper of Rocket.Chat REST API.
    '''

    def __init__(self, url, token=None):
        self.token = token

        if token:
            self.headers = {
                'Content-type': 'application/json',
                'X-Auth-Token': token['authToken'],
                'X-User-Id': token['userId']
            }
        else:
            self.headers = {'Content-type': 'application/json'}

        result = urlparse(url)
        if result.scheme == 'http':
            connection = HTTPConnection
        elif result.scheme == 'https':
            connection = HTTPSConnection
        else:
            raise ValueError(result.scheme)

        self.conn = connection(result.hostname, result.port)

    def __del__(self):
        if self.token is None:
            result = self.GET('logout')
            print(result)

    def __call(self, method, api, **kwargs):
        '''Calls an API.
        '''
        data = json.dumps(kwargs)
        self.conn.request(method, '/api/v1/' + api, data, self.headers)
        response = self.conn.getresponse()

        if response.status != HTTPStatus.OK:
            # pylint: disable=E1120
            status = HTTPStatus(response.status)
            raise HTTPException('%s: %s' % (status.phrase, status.description))

        data = json.loads(response.read(), encoding='utf-8')
        return data

    def POST(self, api, **kwargs):
        '''Call an API with POST.
        '''
        # pylint: disable=C0103
        return self.__call('POST', api, **kwargs)

    def GET(self, api, **kwargs):
        '''Call an API with GET.
        '''
        # pylint: disable=C0103
        return self.__call('GET', api, **kwargs)

    def settoken(self, username, password):
        '''Sets token to HTTP header.
        '''
        result = self.POST('login', username=username, password=password)
        if result['status'] == 'success':
            token = result['data']
            self.headers['X-Auth-Token'] = token['authToken']
            self.headers['X-User-Id'] = token['userId']
        else:
            raise HTTPException(result)
