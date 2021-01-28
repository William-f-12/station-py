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

from abc import ABC, abstractmethod
from typing import Optional

from .dictionary import Map
from .cryptography import key_algorithm
from .asymmetric import VerifyKey


class PublicKey(VerifyKey, ABC):
    """This class is used to en/decrypt symmetric key or sign/verify signature with message data

        Asymmetric Cryptography Public Key
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        key data format: {
            algorithm : "RSA", // "ECC", ...
            data      : "{BASE64_ENCODE}",
            ...
        }
    """

    #
    #   PublicKey factory
    #
    class Factory:

        @abstractmethod
        def parse_public_key(self, key: dict):  # -> Optional[PublicKey]:
            """
            Parse map object to key

            :param key: key info
            :return: PublicKey
            """
            raise NotImplemented

    __factories = {}

    @classmethod
    def register(cls, algorithm: str, factory: Factory):
        cls.__factories[algorithm] = factory

    @classmethod
    def factory(cls, algorithm: str) -> Optional[Factory]:
        return cls.__factories.get(algorithm)

    @classmethod
    def parse(cls, key: dict):  # -> Optional[PublicKey]:
        if key is None:
            return None
        elif isinstance(key, cls):
            return key
        elif isinstance(key, Map):
            key = key.dictionary
        algorithm = key_algorithm(key=key)
        factory = cls.factory(algorithm=algorithm)
        if factory is None:
            factory = cls.factory(algorithm='*')  # unknown
            assert factory is not None, 'cannot parse key: %s' % key
        return factory.parse_public_key(key=key)
