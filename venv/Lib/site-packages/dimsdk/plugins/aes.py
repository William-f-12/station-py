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

import random
from typing import Optional

from Crypto.Cipher import AES

from dimp import base64_encode, base64_decode
from dimp import Dictionary
from dimp import SymmetricKey


def random_bytes(size: int) -> bytes:
    # return bytes(numpy.random.bytes(size))
    bits = random.getrandbits(size * 8)
    return bits.to_bytes(length=size, byteorder='little', signed=False)


class AESKey(Dictionary, SymmetricKey):
    """ AES Key """

    def __init__(self, key: Optional[dict] = None):
        if key is None:
            key = {'algorithm': SymmetricKey.AES}
        super().__init__(dictionary=key)
        self.__data = None
        self.__iv = None

    @property
    def data(self) -> bytes:
        if self.__data is None:
            base64 = self.get('data')
            if base64 is None or len(base64) == 0:
                # generate key data & iv
                data, iv = generate(key_size=self.size, block_size=AES.block_size)
                self.__data = data
                self.__iv = iv
                self['data'] = base64_encode(data=data)
                self['iv'] = base64_encode(data=iv)
                # self['mode'] = 'CBC'
                # self['padding'] = 'PKCS7'
            else:
                self.__data = base64_decode(string=base64)
        return self.__data

    @property
    def iv(self) -> bytes:
        if self.__iv is None:
            base64 = self.get('iv')
            if base64 is None or len(base64) == 0:
                # iv = b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0'
                self.__iv = AES.block_size * chr(0).encode('utf-8')
            else:
                self.__iv = base64_decode(string=base64)
        return self.__iv

    @property
    def size(self) -> int:
        return self.bits >> 3

    @property
    def bits(self) -> int:
        bits = self.get('sizeInBits')
        if bits is None:
            return 256  # AES-256
        else:
            return int(bits)

    def encrypt(self, data: bytes) -> bytes:
        data = pkcs7_pad(data=data, block_size=AES.block_size)
        key = AES.new(self.data, AES.MODE_CBC, self.iv)
        return key.encrypt(data)

    def decrypt(self, data: bytes) -> Optional[bytes]:
        key = AES.new(self.data, AES.MODE_CBC, self.iv)
        plaintext = key.decrypt(data)
        return pkcs7_unpad(data=plaintext)


def generate(key_size: int, block_size: int) -> (bytes, bytes):
    data = random_bytes(key_size)
    iv = random_bytes(block_size)
    return data, iv


def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    assert data is not None, 'data cannot be None'
    amount = block_size - len(data) % block_size
    if amount == 0:
        amount = block_size
    pad = chr(amount).encode('utf-8')
    return data + pad * amount


def pkcs7_unpad(data: bytes) -> bytes:
    assert data is not None and len(data) > 0, 'data empty'
    amount = data[-1]
    assert len(data) >= amount
    return data[:-amount]
