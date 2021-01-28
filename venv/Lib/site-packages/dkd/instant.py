# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao: Universal Message Module
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
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

from abc import abstractmethod
from typing import Optional, List

from mkm.crypto import Map, SymmetricKey
from mkm import ID

from .envelope import Envelope
from .content import Content
from .message import Message, MessageDelegate
from .secure import SecureMessage


class InstantMessage(Message):
    """
        Instant Message
        ~~~~~~~~~~~~~~~

        data format: {
            //-- envelope
            sender   : "moki@xxx",
            receiver : "hulk@yyy",
            time     : 123,
            //-- content
            content  : {...}
        }
    """

    @property
    @abstractmethod
    def content(self) -> Content:
        """ message content """
        raise NotImplemented

    """
        Encrypt the Instant Message to Secure Message
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            +----------+      +----------+
            | sender   |      | sender   |
            | receiver |      | receiver |
            | time     |  ->  | time     |
            |          |      |          |
            | content  |      | data     |  1. data = encrypt(content, PW)
            +----------+      | key/keys |  2. key  = encrypt(PW, receiver.PK)
                              +----------+
    """

    @abstractmethod
    def encrypt(self, password: SymmetricKey, members: Optional[List[ID]]=None) -> Optional[SecureMessage]:
        """
        Encrypt message content with password(symmetric key)

        :param password: A symmetric key for encrypting message content
        :param members:  If this is a group message, get all members here
        :return: SecureMessage object
        """
        raise NotImplemented

    #
    #   InstantMessage factory
    #
    class Factory:

        @abstractmethod
        def create_instant_message(self, head: Envelope, body: Content):  # -> InstantMessage:
            """
            Create instant message with envelope & content

            :param head: message envelope
            :param body: message content
            :return: InstantMessage
            """
            raise NotImplemented

        @abstractmethod
        def parse_instant_message(self, msg: dict):  # -> Optional[InstantMessage]:
            """
            Parse map object to message

            :param msg: message info
            :return: InstantMessage
            """
            raise NotImplemented

    __factory = None

    @classmethod
    def register(cls, factory: Factory):
        cls.__factory = factory

    @classmethod
    def factory(cls) -> Factory:
        return cls.__factory

    @classmethod
    def create(cls, head: Envelope, body: Content):  # -> InstantMessage:
        factory = cls.factory()
        assert factory is not None, 'instant message factory not ready'
        return factory.create_instant_message(head=head, body=body)

    @classmethod
    def parse(cls, msg: dict):  # -> InstantMessage:
        if msg is None:
            return None
        elif isinstance(msg, InstantMessage):
            return msg
        elif isinstance(msg, Map):
            msg = msg.dictionary
        factory = cls.factory()
        assert factory is not None, 'instant message factory not ready'
        return factory.parse_instant_message(msg=msg)


class InstantMessageDelegate(MessageDelegate):

    """ Encrypt Content """

    @abstractmethod
    def serialize_content(self, content: Content, key: SymmetricKey, msg: InstantMessage) -> bytes:
        """
        1. Serialize 'message.content' to data (JsON / ProtoBuf / ...)

        :param content:  message content
        :param key:      symmetric key
        :param msg:      instant message
        :return:         serialized content data
        """
        raise NotImplemented

    @abstractmethod
    def encrypt_content(self, data: bytes, key: SymmetricKey, msg: InstantMessage) -> bytes:
        """
        2. Encrypt content data to 'message.data' with symmetric key

        :param data:     serialized data of message.content
        :param key:      symmetric key
        :param msg:      instant message
        :return:         encrypted message content data
        """
        raise NotImplemented

    @abstractmethod
    def encode_data(self, data: bytes, msg: InstantMessage) -> str:
        """
        3. Encode 'message.data' to String (Base64)

        :param data:     encrypted content data
        :param msg:      instant message
        :return:         string
        """
        raise NotImplemented

    """ Encrypt Key """

    @abstractmethod
    def serialize_key(self, key: SymmetricKey, msg: InstantMessage) -> Optional[bytes]:
        """
        4. Serialize message key to data (JsON / ProtoBuf / ...)

        :param key:      symmetric key to be encrypted
        :param msg:      instant message
        :return:         serialized key data
        """
        raise NotImplemented

    @abstractmethod
    def encrypt_key(self, data: bytes, receiver: ID, msg: InstantMessage) -> Optional[bytes]:
        """
        5. Encrypt key data to 'message.key' with receiver's public key

        :param data:     serialized data of symmetric key
        :param receiver: receiver ID
        :param msg:      instant message
        :return:         encrypted key data
        """
        raise NotImplemented

    @abstractmethod
    def encode_key(self, data: bytes, msg: InstantMessage) -> str:
        """
        6. Encode 'message.key' to String (Base64)

        :param data:     encrypted key data
        :param msg:      instant message
        :return:         base64 string
        """
        raise NotImplemented


"""
    Implements
    ~~~~~~~~~~
"""


def message_content(msg: dict) -> Content:
    content = msg.get('content')
    assert content is not None, 'message content not found: %s' % msg
    return Content.parse(content=content)
