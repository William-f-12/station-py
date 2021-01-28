# -*- coding: utf-8 -*-
#
#   Ming-Ke-Ming : Decentralized User Identity Authentication
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
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
from typing import Optional, Dict

from .crypto import String
from .types import NetworkType, network_is_user, network_is_group


class Address:
    """This class is used to build address for ID

        Address for MKM ID
        ~~~~~~~~~~~~~~~~~~

        properties:
            network - address type
    """

    @property
    @abstractmethod
    def network(self) -> int:
        """
        Get network type of address

        :return: integer as NetworkType
        """
        raise NotImplemented

    @property
    def is_broadcast(self) -> bool:
        # return isinstance(self, BroadcastAddress)
        return False

    @property
    def is_user(self) -> bool:
        return network_is_user(network=self.network)

    @property
    def is_group(self) -> bool:
        return network_is_group(network=self.network)

    #
    #   Address factory
    #
    class Factory:

        @abstractmethod
        def parse_address(self, address: str):  # -> Optional[Address]:
            """
            Parse string object to address

            :param address: address string
            :return: Address
            """
            raise NotImplemented

    __factory = None

    @classmethod
    def register(cls, factory: Factory):
        cls.__factory = factory

    @classmethod
    def factory(cls) -> Factory:
        return cls.__factory

    @classmethod
    def parse(cls, address: str):  # -> Address:
        if address is None:
            return None
        elif isinstance(address, cls):
            return address
        elif isinstance(address, String):
            address = address.string
        factory = cls.factory()
        assert factory is not None, 'address factory not ready'
        return factory.parse_address(address=address)


"""
    Address for broadcast
    ~~~~~~~~~~~~~~~~~~~~~
"""


class BroadcastAddress(String, Address):

    def __init__(self, address: str, network: NetworkType):
        super().__init__(string=address)
        self.__network = network.value

    @property
    def network(self) -> int:
        return self.__network

    @property
    def is_broadcast(self) -> bool:
        return True


ANYWHERE = BroadcastAddress(address='anywhere', network=NetworkType.MAIN)
EVERYWHERE = BroadcastAddress(address='everywhere', network=NetworkType.GROUP)


"""
    Address Factory
    ~~~~~~~~~~~~~~~
"""


class AddressFactory(Address.Factory):

    def __init__(self):
        super().__init__()
        # cache broadcast addresses
        self.__addresses: Dict[str, Address] = {
            str(ANYWHERE): ANYWHERE,
            str(EVERYWHERE): EVERYWHERE,
        }

    def parse_address(self, address: str) -> Optional[Address]:
        add = self.__addresses.get(address)
        if add is None:
            add = self.create_address(address=address)
            if add is not None:
                self.__addresses[address] = add
        return add

    @abstractmethod
    def create_address(self, address: str) -> Optional[Address]:
        """ override for creating address from string """
        raise NotImplemented
