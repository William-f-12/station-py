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
    Daemon Robot
    ~~~~~~~~~~~~

    Robot keep running
"""

import time
from typing import Union

from dimp import ID
from dimp import InstantMessage, Content, TextContent
from dimp import Station

from ..common import Log
from ..common import Facebook

from .robot import Robot
from .chatbot import ChatBot
from .dialog import Dialog


class Daemon(Robot):

    def __init__(self, identifier: ID):
        super().__init__(identifier=identifier)
        # dialog agent
        self.__dialog = Dialog()

    @property
    def bots(self) -> list:
        return self.__dialog.bots

    @bots.setter
    def bots(self, array: Union[list, ChatBot]):
        self.__dialog.bots = array

    def disconnect(self) -> bool:
        if self.messenger is not None:
            if self.messenger.delegate == self.connection:
                self.messenger.delegate = None
        return super().disconnect()

    def connect(self, station: Station) -> bool:
        if not super().connect(station=station):
            self.error('failed to connect station: %s' % station)
            return False
        if self.messenger.delegate is None:
            self.messenger.delegate = self.connection
        self.info('connected to station: %s' % station)
        # handshake after connected
        time.sleep(0.5)
        self.info('%s is shaking hands with %s' % (self.identifier, station))
        return self.handshake()

    def receive_message(self, msg: InstantMessage) -> bool:
        if super().receive_message(msg=msg):
            return True
        facebook: Facebook = self.delegate
        sender = facebook.identifier(msg.envelope.sender)
        if sender.type.is_robot():
            # ignore message from another robot
            return True
        content: Content = msg.content
        response = self.__dialog.query(content=content, sender=sender)
        if response is not None:
            assert isinstance(response, TextContent)
            assert isinstance(content, TextContent)
            nickname = facebook.nickname(identifier=sender)
            question = content.text
            answer = response.text
            group = content.group
            if group is None:
                Log.info('Dialog > %s(%s): "%s" -> "%s"' % (nickname, sender, question, answer))
                return self.send_content(content=response, receiver=sender)
            else:
                group = facebook.identifier(group)
                Log.info('Group Dialog > %s(%s)@%s: "%s" -> "%s"' % (nickname, sender, group.name, question, answer))
                return self.send_content(content=response, receiver=group)