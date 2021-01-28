# -*- coding: utf-8 -*-
#
#   DIM-SDK : Decentralized Instant Messaging Software Development Kit
#
#                                Written in 2020 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2020 Albert Moky
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

import weakref
from typing import Optional, Union

from dimp import ID
from dimp import Content, Envelope, InstantMessage, ReliableMessage
from dimp import Packer

from .delegate import Callback
from .messenger import Messenger, MessageCallback


class MessageTransmitter:

    def __init__(self, messenger: Messenger):
        super().__init__()
        self.__messenger = weakref.ref(messenger)

    @property
    def messenger(self) -> Messenger:
        return self.__messenger()

    @property
    def packer(self) -> Packer:
        return self.messenger.packer

    def send_content(self, sender: ID, receiver: ID, content: Content,
                     callback: Optional[Callback] = None, priority: int = 0) -> bool:
        """
        Send message content to receiver

        :param sender:   sender ID
        :param receiver: receiver ID
        :param content:  message content
        :param callback: if needs callback, set it here
        :param priority: task priority (smaller is faster)
        :return: True on success
        """
        env = Envelope.create(sender=sender, receiver=receiver)
        msg = InstantMessage.create(head=env, body=content)
        return self.send_message(msg=msg, callback=callback, priority=priority)

    def send_message(self, msg: Union[InstantMessage, ReliableMessage],
                     callback: Optional[Callback] = None, priority: int = 0) -> bool:
        """
        Send instant message (encrypt and sign) onto DIM network

        :param msg:      instant message
        :param callback: callback function
        :param priority: task priority
        :return:         False on data/delegate error
        """
        if isinstance(msg, ReliableMessage):
            return self.__send_message(msg=msg, callback=callback, priority=priority)
        assert isinstance(msg, InstantMessage), 'message error: %s' % msg

        # Send message (secured + certified) to target station
        s_msg = self.packer.encrypt_message(msg=msg)
        if s_msg is None:
            # public key not found?
            # raise AssertionError('failed to encrypt message: %s' % msg)
            return False
        r_msg = self.packer.sign_message(msg=s_msg)
        if r_msg is None:
            # TODO: set iMsg.state = error
            raise AssertionError('failed to sign message: %s' % s_msg)

        ok = self.__send_message(msg=r_msg, callback=callback, priority=priority)
        # TODO: if OK, set iMsg.state = sending; else set iMsg.state = waiting

        if not self.messenger.save_message(msg=msg):
            return False
        return ok

    def __send_message(self, msg: ReliableMessage, callback: Optional[Callback] = None, priority: int = 0) -> bool:
        handler = MessageCallback(msg=msg, cb=callback)
        data = self.packer.serialize_message(msg=msg)
        return self.messenger.send_package(data=data, handler=handler, priority=priority)
