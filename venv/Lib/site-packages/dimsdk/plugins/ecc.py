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

import hashlib
from typing import Union, Optional

import ecdsa

from dimp import Dictionary
from dimp import AsymmetricKey, PublicKey, PrivateKey


class ECCPublicKey(Dictionary, PublicKey):
    """ ECC Public Key """

    def __init__(self, key: dict):
        super().__init__(key)
        # data in 'PEM' format
        data = key['data']
        data_len = len(data)
        if data_len == 130 or data_len == 128:
            data = bytes.fromhex(data)
            key = ecdsa.VerifyingKey.from_string(data, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
        else:
            key = ecdsa.VerifyingKey.from_pem(data, hashfunc=hashlib.sha256)
        self.__key = key
        self.__data = key.to_string(encoding='uncompressed')

    @property
    def data(self) -> bytes:
        return self.__data

    @property
    def size(self) -> int:
        return self.bits >> 3

    @property
    def bits(self) -> int:
        bits = self.get('sizeInBits')
        if bits is None:
            return 256  # ECC-256
        else:
            return int(bits)

    def verify(self, data: bytes, signature: bytes) -> bool:
        try:
            return self.__key.verify(signature=signature, data=data,
                                     hashfunc=hashlib.sha256, sigdecode=ecdsa.util.sigdecode_der)
        except ecdsa.BadSignatureError:
            return False


class ECCPrivateKey(Dictionary, PrivateKey):
    """ ECC Private Key """

    def __init__(self, key: Optional[dict] = None):
        if key is None:
            key = {'algorithm': AsymmetricKey.ECC}
        super().__init__(key)
        # data in 'PEM' format
        data = key.get('data')
        if data is None or len(data) == 0:
            # generate private key data
            key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
            data = key.to_string()
            # store private key in PKCS#8 format
            pem = key.to_pem(format='pkcs8').decode('utf-8')
            # pem = data.hex()
            self.__key = key
            self.__data = data
            self['data'] = pem
            self['curve'] = 'SECP256k1'
            self['digest'] = 'SHA256'
        else:
            if len(data) == 64:
                data = bytes.fromhex(data)
                key = ecdsa.SigningKey.from_string(data, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
            else:
                key = ecdsa.SigningKey.from_pem(data, hashfunc=hashlib.sha256)
            self.__key = key
            self.__data = key.to_string()

    @property
    def data(self) -> bytes:
        return self.__data

    @property
    def size(self) -> int:
        return self.bits >> 3

    @property
    def bits(self) -> int:
        bits = self.get('sizeInBits')
        if bits is None:
            return 256  # ECC-256
        else:
            return int(bits)

    @property
    def public_key(self) -> Union[PublicKey]:
        key = self.__key.get_verifying_key()
        # store public key in X.509 format
        pem = key.to_pem().decode('utf-8')
        # pem = key.to_string(encoding='uncompressed').hex()
        info = {
            'algorithm': PublicKey.ECC,
            'data': pem,
            'curve': 'SECP256k1',
            'digest': 'SHA256'
        }
        return ECCPublicKey(info)

    def sign(self, data: bytes) -> bytes:
        return self.__key.sign(data=data, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_der)
