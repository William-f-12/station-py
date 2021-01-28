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

from abc import abstractmethod
from typing import Optional

from .dictionary import Map


class CryptographyKey(Map):
    """Cryptography key with designated algorithm

        Cryptography Key
        ~~~~~~~~~~~~~~~~

        key data format: {
            algorithm : "RSA", // ECC, AES, ...
            data      : "{BASE64_ENCODE}",
            ...
        }
    """

    @property
    def algorithm(self) -> str:
        """
        Get key algorithm name

        :return: algorithm name
        """
        raise NotImplemented

    @property
    @abstractmethod
    def data(self) -> bytes:
        """
        Get key data

        :return: key data
        """
        raise NotImplemented


class EncryptKey(CryptographyKey):

    @abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        """
        ciphertext = encrypt(plaintext, PW)
        ciphertext = encrypt(plaintext, PK)

        :param data: plaintext
        :return:     ciphertext
        """
        raise NotImplemented


class DecryptKey(CryptographyKey):

    @abstractmethod
    def decrypt(self, data: bytes) -> Optional[bytes]:
        """
        plaintext = decrypt(ciphertext, PW);
        plaintext = decrypt(ciphertext, SK);

        :param data: ciphertext
        :return:     plaintext
        """
        raise NotImplemented

    def match(self, key: EncryptKey):
        """
        OK = decrypt(encrypt(data, SK), PK) == data

        :param key: encrypt key
        :return:    False on error
        """
        return keys_match(encrypt_key=key, decrypt_key=self)


def key_algorithm(key: dict) -> str:
    return key.get('algorithm')


promise = 'Moky loves May Lee forever!'.encode('utf-8')


def keys_match(encrypt_key: EncryptKey, decrypt_key: DecryptKey) -> bool:
    return decrypt_key.decrypt(encrypt_key.encrypt(promise)) == promise
