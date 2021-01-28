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

from typing import Optional, Union

from dimp import base58_encode, base58_decode, sha256, ripemd160
from dimp import String
from dimp import Address, NetworkType


class BTCAddress(String, Address):
    """
        Address like BitCoin
        ~~~~~~~~~~~~~~~~~~~~

        data format: "network+digest+code"
            network    --  1 byte
            digest     -- 20 bytes
            check code --  4 bytes

        algorithm:
            fingerprint = PK.data
            digest      = ripemd160(sha256(fingerprint));
            code        = sha256(sha256(network + digest)).prefix(4);
            address     = base58_encode(network + digest + code);
    """

    def __init__(self, address: str, network: Union[NetworkType, int]):
        super().__init__(string=address)
        if isinstance(network, NetworkType):
            self.__network = network.value
        else:
            self.__network = network

    @property
    def network(self) -> int:
        return self.__network

    #
    #   Factory methods
    #
    @classmethod
    def generate(cls, fingerprint: bytes, network: Union[NetworkType, int]) -> Address:
        """
        Generate address with fingerprint and network ID

        :param fingerprint: meta.fingerprint or key.data
        :param network:     address type
        :return: Address object
        """
        if isinstance(network, NetworkType):
            network = network.value
        prefix = chr(network).encode('latin1')
        digest = ripemd160(sha256(fingerprint))
        code = check_code(prefix + digest)
        address = base58_encode(prefix + digest + code)
        return cls(address=address, network=network)

    @classmethod
    def parse(cls, address: str) -> Optional[Address]:
        """
        Parse a string for BTC address

        :param address: address string
        :return: Address object
        """
        prefix_digest_code = base58_decode(address)
        if len(prefix_digest_code) == 25:
            # split them
            prefix = prefix_digest_code[:1]
            digest = prefix_digest_code[1:-4]
            code = prefix_digest_code[-4:]
            # check them
            if check_code(prefix + digest) == code:
                network = ord(prefix)
                return cls(address=address, network=network)


def check_code(data: bytes) -> bytes:
    # check code in BTC address
    return sha256(sha256(data))[:4]
