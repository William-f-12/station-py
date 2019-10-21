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

from mkm.crypto.asymmetric import public_key_classes, private_key_classes

from dimp import PublicKey, PrivateKey


class ECCPublicKey(PublicKey):

    def __init__(self, key: dict):
        super().__init__(key=key)
        # TODO: get public key info

    def encrypt(self, data: bytes) -> bytes:
        # TODO: encrypt plaintext to ciphertext
        pass

    def verify(self, data: bytes, signature: bytes) -> bool:
        # TODO: verify data with signature
        pass


class ECCPrivateKey(PrivateKey):

    def __init__(self, key: dict):
        super().__init__(key=key)
        # TODO: get private key info

    @property
    def public_key(self) -> PublicKey:
        # TODO: get public key from private key
        yield None

    def decrypt(self, data: bytes) -> bytes:
        # TODO: decrypt ciphertext to plaintext
        pass

    def sign(self, data: bytes) -> bytes:
        # TODO: sign data and return the signature
        pass


#
#  register key classes
#

public_key_classes[PublicKey.ECC] = ECCPublicKey

private_key_classes[PrivateKey.ECC] = ECCPrivateKey