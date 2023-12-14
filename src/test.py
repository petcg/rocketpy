#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def test():
    '''Tests REST.
    '''
    rocket = REST('http://hostname:port')
    rocket.settoken('username', 'password')
    result = rocket.POST(
        'chat.postMessage', channel='#general', text='This is a test.')

    print(result)


if __name__ == '__main__':
    test()
