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
    Data Format
    ~~~~~~~~~~~

    Base64, Base58, Hex, UTF-8, JsON
"""

import base64
import json
from abc import abstractmethod
from typing import Optional, Union


class DataCoder:

    @abstractmethod
    def encode(self, data: bytes) -> str:
        """
        Encode binary data to text string

        :param data: binary data
        :return:     text string (Base58/64, Hex, ...)
        """
        raise NotImplemented

    @abstractmethod
    def decode(self, string: str) -> Optional[bytes]:
        """
        Decode text string to binary data

        :param string: text string (Base58/64, Hex, ...)
        :return:       binary data
        """
        raise NotImplemented


class DataParser:

    @abstractmethod
    def encode(self, o: Union[str, dict, list]) -> bytes:
        """
        Encode container/string object to bytes

        :param o: Map, List, or String
        :return: JsON data or UTF-8 string bytes
        """
        raise NotImplemented

    @abstractmethod
    def decode(self, data: bytes) -> Union[str, dict, list, None]:
        """
        Decode bytes to container/string object

        :param data: JsON data or UTF-8 string bytes
        :return: Map, List, or String
        """
        raise NotImplemented


"""
    Interfaces
"""


def base64_encode(data: bytes) -> str:
    return Base64.encode(data)


def base64_decode(string: str) -> Optional[bytes]:
    return Base64.decode(string)


def base58_encode(data: bytes) -> str:
    return Base58.encode(data)


def base58_decode(string: str) -> Optional[bytes]:
    return Base58.decode(string)


def hex_encode(data: bytes) -> str:
    return Hex.encode(data)


def hex_decode(string: str) -> Optional[bytes]:
    return Hex.decode(string)


def json_encode(o: Union[dict, list]) -> bytes:
    return JSON.encode(o=o)


def json_decode(data: bytes) -> Union[dict, list, None]:
    return JSON.decode(data=data)


def utf8_encode(string: str) -> bytes:
    return UTF8.encode(string=string)


def utf8_decode(data: bytes) -> Optional[str]:
    return UTF8.decode(data=data)


"""
    Implementations
    ~~~~~~~~~~~~~~~
    
    Data coders
"""


class B64(DataCoder):

    def encode(self, data: bytes) -> str:
        """ BASE-64 Encode """
        return base64.b64encode(data).decode('utf-8')

    def decode(self, string: str) -> Optional[bytes]:
        """ BASE-64 Decode """
        return base64.b64decode(string)


class H(DataCoder):

    def encode(self, data: bytes) -> str:
        """ HEX Encode """
        # return binascii.b2a_hex(data).decode('utf-8')
        return data.hex()

    def decode(self, string: str) -> Optional[bytes]:
        """ HEX Decode """
        # return binascii.a2b_hex(string)
        return bytes.fromhex(string)


class Base64:
    coder: DataCoder = B64()

    @staticmethod
    def encode(data: bytes) -> str:
        assert Base64.coder is not None, 'Base64 coder not set yet'
        return Base64.coder.encode(data=data)

    @staticmethod
    def decode(string: str) -> Optional[bytes]:
        assert Base64.coder is not None, 'Base64 coder not set yet'
        return Base64.coder.decode(string=string)


class Base58:
    coder: DataCoder = None

    @staticmethod
    def encode(data: bytes) -> str:
        assert Base58.coder is not None, 'Base58 coder not set yet'
        return Base58.coder.encode(data=data)

    @staticmethod
    def decode(string: str) -> Optional[bytes]:
        assert Base58.coder is not None, 'Base58 coder not set yet'
        return Base58.coder.decode(string=string)


class Hex:
    coder: DataCoder = H()

    @staticmethod
    def encode(data: bytes) -> str:
        assert Hex.coder is not None, 'Hex coder not set yet'
        return Hex.coder.encode(data=data)

    @staticmethod
    def decode(string: str) -> Optional[bytes]:
        assert Hex.coder is not None, 'Hex coder not set yet'
        return Hex.coder.decode(string=string)


"""
    Implementations
    ~~~~~~~~~~~~~~~

    Data parsers
"""


class J(DataParser):

    def encode(self, o: Union[dict, list]) -> bytes:
        """ JsON encode """
        return bytes(json.dumps(o), encoding='utf-8')

    def decode(self, data: bytes) -> Union[dict, list, None]:
        """ JsON decode """
        return json.loads(data)


class U(DataParser):

    def encode(self, o: str) -> bytes:
        """ UTF-8 encode """
        return o.encode('utf-8')

    def decode(self, data: bytes) -> Optional[str]:
        """ UTF-8 decode """
        return data.decode('utf-8')


class JSON:
    parser: DataParser = J()

    @staticmethod
    def encode(o: Union[dict, list]) -> bytes:
        assert JSON.parser is not None, 'JSON parser not set yet'
        return JSON.parser.encode(o=o)

    @staticmethod
    def decode(data: bytes) -> Union[dict, list, None]:
        assert JSON.parser is not None, 'JSON parser not set yet'
        return JSON.parser.decode(data=data)


class UTF8:
    parser: DataParser = U()

    @staticmethod
    def encode(string: str) -> bytes:
        assert UTF8.parser is not None, 'UTF8 parser not set yet'
        return UTF8.parser.encode(o=string)

    @staticmethod
    def decode(data: bytes) -> Optional[str]:
        assert UTF8.parser is not None, 'UTF8 parser not set yet'
        return UTF8.parser.decode(data=data)
