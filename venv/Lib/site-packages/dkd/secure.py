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

from .content import Content
from .message import Message, MessageDelegate


class SecureMessage(Message):
    """Instant Message encrypted by a symmetric key

        Secure Message
        ~~~~~~~~~~~~~~

        data format: {
            //-- envelope
            sender   : "moki@xxx",
            receiver : "hulk@yyy",
            time     : 123,
            //-- content data & key/keys
            data     : "...",  // base64_encode(symmetric)
            key      : "...",  // base64_encode(asymmetric)
            keys     : {
                "ID1": "key1", // base64_encode(asymmetric)
            }
        }
    """

    @property
    @abstractmethod
    def data(self) -> bytes:
        """ encrypted message content """
        raise NotImplemented

    @property
    @abstractmethod
    def encrypted_key(self) -> Optional[bytes]:
        """ encrypted message key """
        raise NotImplemented

    @property
    def encrypted_keys(self) -> Optional[dict]:
        """ encrypted message keys """
        raise NotImplemented

    """
        Decrypt the Secure Message to Instant Message
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            +----------+      +----------+
            | sender   |      | sender   |
            | receiver |      | receiver |
            | time     |  ->  | time     |
            |          |      |          |  1. PW      = decrypt(key, receiver.SK)
            | data     |      | content  |  2. content = decrypt(data, PW)
            | key/keys |      +----------+
            +----------+
    """

    @abstractmethod
    def decrypt(self):  # -> Optional[InstantMessage]:
        """
        Decrypt message data to plaintext content

        :return: InstantMessage object
        """
        raise NotImplemented

    """
        Sign the Secure Message to Reliable Message
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            +----------+      +----------+
            | sender   |      | sender   |
            | receiver |      | receiver |
            | time     |  ->  | time     |
            |          |      |          |
            | data     |      | data     |
            | key/keys |      | key/keys |
            +----------+      | signature|  1. signature = sign(data, sender.SK)
                              +----------+
    """

    def sign(self):  # -> ReliableMessage:
        """
        Sign the message.data with sender's private key

        :return: ReliableMessage object
        """
        raise NotImplemented

    """
        Split/Trim group message
        ~~~~~~~~~~~~~~~~~~~~~~~~

        for each members, get key from 'keys' and replace 'receiver' to member ID
    """

    def split(self, members: List[ID]):  # -> List[SecureMessage]:
        """
        Split the group message to single person messages

        :param members: All group members
        :return:        A list of SecureMessage objects for all group members
        """
        raise NotImplemented

    def trim(self, member: ID):  # -> SecureMessage
        """
        Trim the group message for a member

        :param member: Member ID
        :return:       A SecureMessage object drop all irrelevant keys to the member
        """
        raise NotImplemented

    #
    #   SecureMessage factory
    #
    class Factory:

        @abstractmethod
        def parse_secure_message(self, msg: dict):  # -> Optional[SecureMessage]:
            """
            Parse map object to message

            :param msg: message info
            :return: SecureMessage
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
    def parse(cls, msg: dict):  # -> SecureMessage:
        if msg is None:
            return None
        elif isinstance(msg, SecureMessage):
            return msg
        elif isinstance(msg, Map):
            msg = msg.dictionary
        factory = cls.factory()
        assert factory is not None, 'secure message factory not ready'
        return factory.parse_secure_message(msg=msg)


class SecureMessageDelegate(MessageDelegate):

    """ Delegate for SecureMessage """

    """ Decrypt Key """

    @abstractmethod
    def decode_key(self, key: str, msg: SecureMessage) -> Optional[bytes]:
        """
        1. Decode 'message.key' to encrypted symmetric key data

        :param key:      base64 string
        :param msg:      secure message
        :return:         encrypted symmetric key data
        """
        raise NotImplemented

    @abstractmethod
    def decrypt_key(self, data: bytes, sender: ID, receiver: ID, msg: SecureMessage) -> Optional[bytes]:
        """
        2. Decrypt 'message.key' with receiver's private key

        :param data:     encrypted symmetric key data
        :param sender:   sender/member ID
        :param receiver: receiver/group ID
        :param msg:      secure message
        :return:         serialized data of symmetric key
        """
        raise NotImplemented

    @abstractmethod
    def deserialize_key(self, data: Optional[bytes], sender: ID, receiver: ID, msg: SecureMessage) -> SymmetricKey:
        """
        3. Deserialize message key from data (JsON / ProtoBuf / ...)

        :param data:     serialized key data
        :param sender:   sender/member ID
        :param receiver: receiver/group ID
        :param msg:      secure message
        :return:         symmetric key
        """
        raise NotImplemented

    """ Decrypt Content """

    @abstractmethod
    def decode_data(self, data: str, msg: SecureMessage) -> Optional[bytes]:
        """
        4. Decode 'message.data' to encrypted content data

        :param data:     base64 string
        :param msg:      secure message
        :return:         encrypted content data
        """
        raise NotImplemented

    @abstractmethod
    def decrypt_content(self, data: bytes, key: SymmetricKey, msg: SecureMessage) -> Optional[bytes]:
        """
        5. Decrypt 'message.data' with symmetric key

        :param data:     encrypted content data
        :param key:      symmetric key
        :param msg:      secure message
        :return:         serialized data of message content
        """
        raise NotImplemented

    @abstractmethod
    def deserialize_content(self, data: bytes, key: SymmetricKey, msg: SecureMessage) -> Optional[Content]:
        """
        6. Deserialize message content from data (JsON / ProtoBuf / ...)

        :param data:     serialized content data
        :param key:      symmetric key
        :param msg:      secure message
        :return:         message content
        """
        raise NotImplemented

    """ Signature """

    @abstractmethod
    def sign_data(self, data: bytes, sender: ID, msg: SecureMessage) -> bytes:
        """
        1. Sign 'message.data' with sender's private key

        :param data:      encrypted message data
        :param sender:    sender ID
        :param msg:       secure message
        :return:          signature of encrypted message data
        """
        raise NotImplemented

    @abstractmethod
    def encode_signature(self, signature: bytes, msg: SecureMessage) -> str:
        """
        2. Encode 'message.signature' to String (Base64)

        :param signature: signature of message.data
        :param msg:       secure message
        :return:          string
        """
        raise NotImplemented
