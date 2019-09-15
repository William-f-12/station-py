#! /usr/bin/env python
# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

"""
    DIM Client
    ~~~~~~~~~~

    Simple client for testing
"""

import json
from cmd import Cmd
from time import sleep

from dimp import ID, Profile
from dimp import Content, ContentType, TextContent
from dimp import Command, ProfileCommand
from dimp import InstantMessage
from dimp import Station

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from common import Robot
from common.immortals import moki, hulk

from station.config import g_database, g_facebook, g_ans, g_messenger
from station.config import current_station


"""
    Current Station
    ~~~~~~~~~~~~~~~
"""
g_station = current_station

g_station.host = '127.0.0.1'
# g_station.host = '124.156.108.150'  # dimchat-hk
# g_station.host = '134.175.87.98'  # dimchat-gz
g_station.port = 9394

g_database.base_dir = '/tmp/.dim/'

# Address Name Service
g_ans.save_record('moki', moki.identifier)
g_ans.save_record('hulk', hulk.identifier)
g_ans.save_record('station', g_station.identifier)


class Client(Robot):

    def __init__(self, identifier: ID):
        super().__init__(identifier=identifier)
        # station connection
        self.delegate = g_facebook
        self.messenger = g_messenger

    def disconnect(self) -> bool:
        if g_messenger.delegate == self.connection:
            g_messenger.delegate = None
        return super().disconnect()

    def connect(self, station: Station) -> bool:
        if not super().connect(station=station):
            self.error('failed to connect station: %s' % station)
            return False
        if g_messenger.delegate is None:
            g_messenger.delegate = self.connection
        self.info('connected to station: %s' % station)
        # handshake after connected
        sleep(0.5)
        self.info('%s is shaking hands with %s' % (self.identifier, station))
        return self.handshake()

    def execute(self, cmd: Command, sender: ID) -> bool:
        if super().execute(cmd=cmd, sender=sender):
            return True
        command = cmd.command
        if 'search' == command:
            self.info('##### received search response')
            if 'users' in cmd:
                users = cmd['users']
                print('      users:', json.dumps(users))
            if 'results' in cmd:
                results = cmd['results']
                print('      results:', results)
        elif 'users' == command:
            self.info('##### online users: %s' % cmd.get('message'))
            if 'users' in cmd:
                users = cmd['users']
                print('      users:', json.dumps(users))
        else:
            self.info('***** command from "%s": %s (%s)' % (sender.name, cmd['command'], cmd))

    def receive_message(self, msg: InstantMessage) -> bool:
        if super().receive_message(msg=msg):
            return True
        sender = g_facebook.identifier(msg.envelope.sender)
        content: Content = msg.content
        if content.type == ContentType.Text:
            self.info('***** Message from "%s": %s' % (sender.name, content['text']))
        else:
            self.info('!!!!! Message from "%s": %s' % (sender.name, content))


class Console(Cmd):

    prompt = '[DIM] > '
    intro = '\n\tWelcome to DIM world!\n'

    def __init__(self):
        super().__init__()
        self.client: Client = None
        self.receiver = None
        self.do_call('station')

    @staticmethod
    def info(msg: str):
        print('\r%s' % msg)

    def login(self, identifier: ID):
        # logout first
        self.logout()
        # login with user ID
        self.info('connecting to %s ...' % g_station)
        client = Client(identifier=identifier)
        client.connect(station=g_station)
        self.client = client
        if self.receiver is None:
            self.receiver = client.station.identifier

    def logout(self):
        client = self.client
        if client:
            self.info('disconnect from %s ...' % client.station)
            client.disconnect()
            self.client = None
        self.receiver = None

    def emptyline(self):
        print('')
        print('    Usage:')
        print('        login <ID>        - switch user (must say "hello" twice after login)')
        print('        logout            - clear session')
        print('        show users        - list online users')
        print('        search <number>   - search users by number')
        print('        profile <ID>      - query profile with ID')
        print('        call <ID>         - change receiver to another user (or "station")')
        print('        send <text>       - send message')
        print('        exit              - terminate')
        print('')
        if self.client:
            if self.receiver:
                print('You(%s) are talking with "%s" now.' % (self.client.identifier, self.receiver))
            else:
                print('%s is login in' % self.client.identifier)

    def do_exit(self, arg):
        if self.client:
            self.client.disconnect()
            self.client = None
        print('Bye!')
        return True

    def do_login(self, name: str):
        sender = g_facebook.identifier(name)
        if sender is None:
            self.info('unknown user: %s' % name)
        else:
            self.info('login as %s' % sender)
            self.login(identifier=sender)
            self.prompt = Console.prompt + sender.name + '$ '

    def do_logout(self, arg):
        if self.client is None:
            self.info('not login yet')
        else:
            self.info('%s logout' % self.client.identifier)
            self.logout()
        self.prompt = Console.prompt

    def do_call(self, name: str):
        if self.client is None:
            self.info('login first')
            return
        receiver = g_facebook.identifier(name)
        if receiver is None:
            self.info('unknown user: %s' % name)
        else:
            self.info('talking with %s now' % receiver)
            self.client.check_meta(identifier=receiver)
            # switch receiver
            self.receiver = receiver

    def do_send(self, msg: str):
        if self.client is None:
            self.info('login first')
            return
        if len(msg) > 0:
            content = TextContent.new(text=msg)
            self.client.send_content(content=content, receiver=self.receiver)

    def do_show(self, name: str):
        if self.client is None:
            self.info('login first')
            return
        if 'users' == name:
            cmd: Command = Command.new(command='users')
            self.client.send_command(cmd=cmd)
        else:
            self.info('I don\'t understand.')

    def do_search(self, keywords: str):
        if self.client is None:
            self.info('login first')
            return
        cmd: Command = Command.new(command='search')
        cmd['keywords'] = keywords
        self.client.send_command(cmd=cmd)

    def do_profile(self, name: str):
        if self.client is None:
            self.info('login first')
            return
        profile = None
        if name is None:
            identifier = self.client.identifier
        elif name.startswith('{') and name.endswith('}'):
            identifier = self.client.identifier
            profile = json.loads(name)
        else:
            identifier = g_facebook.identifier(name)
            if identifier is None:
                self.info('I don\'t understand.')
                return
        if profile:
            private_key = g_facebook.private_key_for_signature(identifier=self.client.identifier)
            assert private_key is not None, 'failed to get private key for client: %s' % self.client
            # create new profile and set all properties
            tai = Profile.new(identifier=identifier)
            for key in profile:
                tai.set_property(key, profile.get(key))
            tai.sign(private_key)
            cmd = ProfileCommand.response(identifier=identifier, profile=tai)
        else:
            cmd = ProfileCommand.query(identifier=identifier)
        self.client.send_command(cmd=cmd)


if __name__ == '__main__':

    console = Console()
    console.cmdloop()
