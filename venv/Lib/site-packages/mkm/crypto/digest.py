# -*- coding: utf-8 -*-
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

"""
    Data Digest
    ~~~~~~~~~~~

    MD5, SHA-256, RipeMD-160
"""

import hashlib
from abc import abstractmethod


class DataDigester:

    @abstractmethod
    def digest(self, data: bytes) -> bytes:
        raise NotImplemented


"""
    Interfaces
"""


def md5(data: bytes) -> bytes:
    return MD5.digest(data=data)


def sha1(data: bytes) -> bytes:
    return SHA1.digest(data=data)


def sha256(data: bytes) -> bytes:
    return SHA256.digest(data=data)


def keccak256(data: bytes) -> bytes:
    return KECCAK256.digest(data=data)


def ripemd160(data: bytes) -> bytes:
    return RIPEMD160.digest(data=data)


"""
    Implementations
"""


class M5(DataDigester):

    def digest(self, data: bytes) -> bytes:
        """ MD5 digest """
        hash_obj = hashlib.md5()
        hash_obj.update(data)
        return hash_obj.digest()


class S1(DataDigester):

    def digest(self, data: bytes) -> bytes:
        """ SHA1 Digest """
        return hashlib.sha1(data).digest()


class S256(DataDigester):

    def digest(self, data: bytes) -> bytes:
        """ SHA-256 """
        return hashlib.sha256(data).digest()


class R160(DataDigester):

    def digest(self, data: bytes) -> bytes:
        """ RIPEMD-160 """
        hash_obj = hashlib.new('ripemd160')
        hash_obj.update(data)
        return hash_obj.digest()


class MD5:
    digester: DataDigester = M5()

    @staticmethod
    def digest(data: bytes) -> bytes:
        assert MD5.digester is not None, 'MD5 coder not set yet'
        return MD5.digester.digest(data=data)


class SHA1:
    digester: DataDigester = S1()

    @staticmethod
    def digest(data: bytes) -> bytes:
        assert SHA1.digester is not None, 'SHA1 coder not set yet'
        return SHA1.digester.digest(data=data)


class SHA256:
    digester: DataDigester = S256()

    @staticmethod
    def digest(data: bytes) -> bytes:
        assert SHA256.digester is not None, 'SHA256 coder not set yet'
        return SHA256.digester.digest(data=data)


class KECCAK256:
    digester: DataDigester = None

    @staticmethod
    def digest(data: bytes) -> bytes:
        assert KECCAK256.digester is not None, 'KECCAK256 coder not set yet'
        return KECCAK256.digester.digest(data=data)


class RIPEMD160:
    digester: DataDigester = R160()

    @staticmethod
    def digest(data: bytes) -> bytes:
        assert RIPEMD160.digester is not None, 'RIPEMD160 coder not set yet'
        return RIPEMD160.digester.digest(data=data)
