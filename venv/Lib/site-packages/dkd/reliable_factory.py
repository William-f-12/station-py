# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao: Universal Message Module
#
#                                Written in 2021 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2021 Albert Moky
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

from typing import Optional

from mkm import Meta, Visa

from .secure import SecureMessage
from .secure_factory import EncryptedMessage
from .reliable import ReliableMessage, ReliableMessageDelegate
from .reliable import message_meta, message_set_visa, message_visa, message_set_meta


"""
    ReliableMessage Factory
    ~~~~~~~~~~~~~~~~~~~~~~~
"""


class ReliableMessageFactory(ReliableMessage.Factory):

    def parse_reliable_message(self, msg: dict) -> Optional[ReliableMessage]:
        return NetworkMessage(msg=msg)


# register SecureMessage factory
ReliableMessage.register(factory=ReliableMessageFactory())


class NetworkMessage(EncryptedMessage, ReliableMessage):

    def __init__(self, msg: dict):
        super().__init__(msg=msg)
        # lazy
        self.__signature = None
        self.__meta = None
        self.__visa = None

    @property
    def signature(self) -> bytes:
        if self.__signature is None:
            base64 = self.get('signature')
            assert base64 is not None, 'signature of reliable message cannot be empty: %s' % self
            delegate = self.delegate
            assert isinstance(delegate, ReliableMessageDelegate), 'reliable delegate error: %s' % delegate
            self.__signature = delegate.decode_signature(signature=base64, msg=self)
        return self.__signature

    @property
    def meta(self) -> Optional[Meta]:
        if self.__meta is None:
            self.__meta = message_meta(msg=self.dictionary)
        return self.__meta

    @meta.setter
    def meta(self, value: Meta):
        message_set_meta(msg=self.dictionary, meta=value)
        self.__meta = value

    @property
    def visa(self) -> Optional[Visa]:
        if self.__visa is None:
            self.__visa = message_visa(msg=self.dictionary)
        return self.__visa

    @visa.setter
    def visa(self, value: Visa):
        message_set_visa(msg=self.dictionary, visa=value)
        self.__visa = value

    def verify(self) -> Optional[SecureMessage]:
        data = self.data
        if data is None:
            raise ValueError('failed to decode content data: %s' % self)
        signature = self.signature
        if signature is None:
            raise ValueError('failed to decode message signature: %s' % self)
        # 1. verify data signature
        delegate = self.delegate
        assert isinstance(delegate, ReliableMessageDelegate), 'reliable delegate error: %s' % delegate
        if delegate.verify_data_signature(data=data, signature=signature, sender=self.sender, msg=self):
            # 2. pack message
            msg = self.copy_dictionary()
            msg.pop('signature')  # remove 'signature'
            return SecureMessage.parse(msg=msg)
        # else:
        #     raise ValueError('Signature error: %s' % self)
