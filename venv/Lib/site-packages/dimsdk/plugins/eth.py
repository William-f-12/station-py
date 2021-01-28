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

from typing import Optional

from dimp import hex_encode, keccak256
from dimp import String
from dimp import Address, NetworkType


class ETHAddress(String, Address):
    """
        Address like Ethereum
        ~~~~~~~~~~~~~~~~~~~~~

        data format: "0x{address}"

        algorithm:
            fingerprint = PK.data
            digest      = keccak256(fingerprint)
            address     = hex_encode(digest.suffix(20))
    """

    def __init__(self, address: str):
        super().__init__(string=address)

    @property
    def network(self) -> int:
        return NetworkType.MAIN.value

    @classmethod
    def validate_address(cls, address: str) -> Optional[str]:
        if is_eth(address=address):
            lower = address[2:].lower()
            return '0x' + eip55(address=lower)

    @classmethod
    def is_validate(cls, address: str) -> bool:
        return cls.validate_address(address=address) == address

    #
    #   Factory methods
    #
    @classmethod
    def generate(cls, fingerprint: bytes) -> Address:
        """
        Generate ETH address with key.data

        :param fingerprint: key.data
        :return: Address object
        """
        if len(fingerprint) == 65:
            fingerprint = fingerprint[1:]
        assert len(fingerprint) == 64, 'key data length error: %d' % len(fingerprint)
        # 1. digest = keccak256(fingerprint)
        digest = keccak256(data=fingerprint)
        # 2. address = hex_encode(digest.suffix(20))
        tail = digest[-20:]
        address = '0x' + eip55(address=hex_encode(data=tail))
        return cls(address=address)

    @classmethod
    def parse(cls, address: str) -> Optional[Address]:
        """
        Parse a string for ETH address

        :param address: address string
        :return: Address object
        """
        if is_eth(address=address):
            return cls(address=address)


# https://eips.ethereum.org/EIPS/eip-55
def eip55(address: str) -> str:
    res = ''
    table = keccak256(address.encode('utf-8'))
    for i in range(40):
        ch = address[i]
        x = ord(ch)
        if x > 0x39:
            # check for each 4 bits in the hash table
            # if the first bit is '1',
            #     change the character to uppercase
            x -= (table[i >> 1] << (i << 2 & 4) & 0x80) >> 2
            ch = chr(x)
        res += ch
    return res


def is_eth(address: str) -> bool:
    if len(address) != 42:
        return False
    if address[0] != '0' or address[1] != 'x':
        return False
    for i in range(2, 42):
        ch = address[i]
        if '0' <= ch <= '9':
            continue
        if 'A' <= ch <= 'Z':
            continue
        if 'a' <= ch <= 'z':
            continue
        # unexpected character
        return False
    return True
