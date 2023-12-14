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

    @classmethod
    def fromlogin(cls, url, login):
        '''Login using username/password and return REST object.
        '''
        # pylint: disable=W0212
        rest = cls(url)
        result = rest.POST('login', **login)
        if result['status'] == 'success':
            token = result['data']
            rest.__headers.update({
                'X-Auth-Token': token['authToken'],
                'X-User-Id': token['userId'],
            })
        else:
            raise HTTPException(result)

        print('login')
        return rest

    @classmethod
    def fromtoken(cls, url, token):
        '''Return REST object with specified token.
        '''
        # pylint: disable=W0212
        rest = cls(url)
        rest.__headers.update({
            'X-Auth-Token': token['authToken'],
            'X-User-Id': token['userId'],
        })

    def __init__(self, url):
        result = urlparse(url)
        if result.scheme == 'http':
            connection = HTTPConnection
        elif result.scheme == 'https':
            connection = HTTPSConnection
        else:
            raise ValueError(result.scheme)

        self.__conn = connection(result.hostname, result.port)
        self.__headers = {'Content-type': 'application/json'}

    def __del__(self):
        try:
            self.GET('logout')
        except HTTPException:
            pass
        else:
            print('logout')

    def __call(self, method, api, **kwargs):
        '''Calls an API.
        '''
        data = json.dumps(kwargs)
        conn = self.__conn
        conn.request(method, '/api/v1/' + api, data, self.__headers)
        response = conn.getresponse()

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
