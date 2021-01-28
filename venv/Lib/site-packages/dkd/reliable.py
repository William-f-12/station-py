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
from typing import Optional

from mkm.crypto import Map
from mkm import ID, Meta, Visa, Document

from .secure import SecureMessage, SecureMessageDelegate


class ReliableMessage(SecureMessage):
    """This class is used to sign the SecureMessage
    It contains a 'signature' field which signed with sender's private key

        Instant Message signed by an asymmetric key
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            //-- envelope
            sender   : "moki@xxx",
            receiver : "hulk@yyy",
            time     : 123,
            //-- content data and key/keys
            data     : "...",  // base64_encode(symmetric)
            key      : "...",  // base64_encode(asymmetric)
            keys     : {
                "ID1": "key1", // base64_encode(asymmetric)
            },
            //-- signature
            signature: "..."   // base64_encode()
        }
    """

    @property
    @abstractmethod
    def signature(self) -> bytes:
        """ signature for encrypted data of message content """
        raise NotImplemented

    @property
    @abstractmethod
    def meta(self) -> Optional[Meta]:
        """
            Sender's Meta
            ~~~~~~~~~~~~~
            Extends for the first message package of 'Handshake' protocol.
        """
        raise NotImplemented

    @meta.setter
    @abstractmethod
    def meta(self, value: Meta):
        raise NotImplemented

    @property
    @abstractmethod
    def visa(self) -> Optional[Visa]:
        """
            Sender's Visa Document
            ~~~~~~~~~~~~~~~~~~~~~~
            Extends for the first message package of 'Handshake' protocol.
        """
        raise NotImplemented

    @visa.setter
    @abstractmethod
    def visa(self, value: Visa):
        raise NotImplemented

    """
        Verify the Reliable Message to Secure Message
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            +----------+      +----------+
            | sender   |      | sender   |
            | receiver |      | receiver |
            | time     |  ->  | time     |
            |          |      |          |
            | data     |      | data     |  1. verify(data, signature, sender.PK)
            | key/keys |      | key/keys |
            | signature|      +----------+
            +----------+
    """

    def verify(self) -> Optional[SecureMessage]:
        """
        Verify the message.data with signature

        :return: SecureMessage object if signature matched
        """
        raise NotImplemented

    #
    #   ReliableMessage factory
    #
    class Factory:

        @abstractmethod
        def parse_reliable_message(self, msg: dict):  # -> Optional[ReliableMessage]:
            """
            Parse map object to message

            :param msg: message info
            :return: ReliableMessage
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
    def parse(cls, msg: dict):  # -> ReliableMessage:
        if msg is None:
            return None
        elif isinstance(msg, ReliableMessage):
            return msg
        elif isinstance(msg, Map):
            msg = msg.dictionary
        factory = cls.factory()
        assert factory is not None, 'reliable message factory not ready'
        return factory.parse_reliable_message(msg=msg)


class ReliableMessageDelegate(SecureMessageDelegate):

    @abstractmethod
    def decode_signature(self, signature: str, msg: ReliableMessage) -> Optional[bytes]:
        """
        1. Decode 'message.signature' from String (Base64)

        :param signature: base64 string
        :param msg:       reliable message
        :return:          signature data
        """
        raise NotImplemented

    @abstractmethod
    def verify_data_signature(self, data: bytes, signature: bytes, sender: ID, msg: ReliableMessage) -> bool:
        """
        2. Verify the message data and signature with sender's public key

        :param data:      message content(encrypted) data
        :param signature: signature of message content(encrypted) data
        :param sender:    sender ID
        :param msg:       reliable message
        :return:          True on signature matched
        """
        raise NotImplemented


"""
    Implements
    ~~~~~~~~~~
"""


def message_meta(msg: dict) -> Optional[Meta]:
    meta = msg.get('meta')
    return Meta.parse(meta=meta)


def message_set_meta(msg: dict, meta: Meta):
    if meta is None:
        msg.pop('meta', None)
    else:
        msg['meta'] = meta.dictionary


def message_visa(msg: dict) -> Optional[Visa]:
    visa = msg.get('visa')
    if visa is None:
        visa = msg.get('profile')
    return Document.parse(document=visa)


def message_set_visa(msg: dict, visa: Visa):
    msg.pop('profile', None)
    if visa is None:
        msg.pop('visa', None)
    else:
        msg['visa'] = visa.dictionary
