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

"""
    Crypto
    ~~~~~~

    Crypto Keys: SymmetricKey, PrivateKey, PublicKey
"""

from .format import *
from .digest import *

from .dictionary import Wrapper, Array, Map, Dictionary
from .string import String

from .cryptography import CryptographyKey
from .symmetric import SymmetricKey, EncryptKey, DecryptKey
from .asymmetric import AsymmetricKey, SignKey, VerifyKey
from .public import PublicKey
from .private import PrivateKey


__all__ = [

    # Data Format
    'DataCoder', 'Base64', 'Base58', 'Hex',
    'base64_encode', 'base64_decode', 'base58_encode', 'base58_decode', 'hex_encode', 'hex_decode',
    'DataParser', 'JSON', 'UTF8',
    'json_encode', 'json_decode', 'utf8_encode', 'utf8_decode',

    # Data Digest
    'DataDigester', 'MD5', 'SHA1', 'SHA256', 'KECCAK256', 'RIPEMD160',
    'md5', 'sha1', 'sha256', 'keccak256', 'ripemd160',

    # Types
    'Wrapper', 'Array', 'Map', 'Dictionary', 'String',

    # Crypto
    'CryptographyKey',
    'SymmetricKey', 'EncryptKey', 'DecryptKey',
    'AsymmetricKey', 'SignKey', 'VerifyKey',
    'PublicKey', 'PrivateKey',
]
