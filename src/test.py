#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
'''

import argparse
import json
import rocketpy


def test():
    '''Tests REST.
    '''

    def _parseargs():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--host', required=True, help='e.g. https://open.rocket.chat')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--login')
        group.add_argument('--token')
        parser.add_argument('--channel', required=True, help='e.g. #sandbox')
        return parser.parse_args()

    args = _parseargs()

    if args.login:
        print('login:', args.login)
        login = json.loads(args.login)
        rocket = rocketpy.REST.fromlogin(args.host, login)
    elif args.token:
        print('token:', args.token)
        token = json.loads(args.token)
        rocket = rocketpy.REST.fromtoken(args.host, token)

    channel = args.channel
    if not channel.startswith('#'):
        channel = '#' + channel

    result = rocket.POST(
        'chat.postMessage', channel=channel, text='This is a test.')

    print(result)


if __name__ == '__main__':
    test()
