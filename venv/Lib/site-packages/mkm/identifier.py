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
from typing import Optional

from .crypto import String
from .address import Address, ANYWHERE, EVERYWHERE


class ID:
    """
        ID for entity (User/Group)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: "name@address[/terminal]"

        fields:
            name     - entity name, the seed of fingerprint to generate address
            address  - a string to identify an entity
            terminal - entity login resource(device), OPTIONAL
    """

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        if not isinstance(other, ID):
            if isinstance(other, String):
                other = other.string
            assert isinstance(other, str), 'ID error: %s' % other
            other = ID.parse(identifier=other)
            if other is None:
                return False
        if self is other:
            # same object
            return True
        return self.address == other.address and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.address)

    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        raise NotImplemented

    @property
    @abstractmethod
    def address(self) -> Address:
        raise NotImplemented

    @property
    @abstractmethod
    def terminal(self) -> Optional[str]:
        raise NotImplemented

    @property
    def type(self) -> int:
        """ ID type """
        return self.address.network

    @property
    def is_broadcast(self) -> bool:
        return self.address.is_broadcast

    @property
    def is_user(self) -> bool:
        return self.address.is_user

    @property
    def is_group(self) -> bool:
        return self.address.is_group

    @classmethod
    def convert(cls, members: list) -> list:
        """
        Convert ID list from string array

        :param members: string array
        :return: ID list
        """
        array = []
        for item in members:
            identifier = cls.parse(identifier=item)
            if identifier is None:
                continue
            array.append(identifier)
        return array

    @classmethod
    def revert(cls, members: list) -> list:
        """
        Revert ID list to string array

        :param members: ID list
        :return: string array
        """
        array = []
        for item in members:
            array.append(str(item))
        return array

    #
    #   ID factory
    #
    class Factory:

        @abstractmethod
        def create_identifier(self, address: Address, name: Optional[str]=None, terminal: Optional[str]=None):  # -> ID:
            """
            Create ID

            :param address:  ID.address
            :param name:     ID.name
            :param terminal: ID.terminal
            :return: ID
            """
            raise NotImplemented

        @abstractmethod
        def parse_identifier(self, identifier: str):  # -> Optional[ID]:
            """
            Parse string object to ID

            :param identifier: ID string
            :return: ID
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
    def create(cls, address: Address, name: Optional[str]=None, terminal: Optional[str]=None):  # -> Optional[ID]:
        factory = cls.factory()
        assert factory is not None, 'ID factory not ready'
        return factory.create_identifier(address=address, name=name, terminal=terminal)

    @classmethod
    def parse(cls, identifier: str):  # -> Optional[ID]:
        if identifier is None:
            return None
        elif isinstance(identifier, cls):
            return identifier
        elif isinstance(identifier, String):
            identifier = identifier.string
        factory = cls.factory()
        assert factory is not None, 'ID factory not ready'
        return factory.parse_identifier(identifier=identifier)


"""
    Implements
    ~~~~~~~~~~
"""


def parse(string: str) -> Optional[ID]:
    # split ID string
    pair = string.split('/', 1)
    # terminal
    if len(pair) == 1:
        # no terminal
        terminal = None
    else:
        # got terminal
        terminal = pair[1]
    # name @ address
    assert len(pair[0]) > 0, 'ID error: %s' % string
    pair = pair[0].split('@', 1)
    if len(pair) == 1:
        # got address without name
        name = None
        address = Address.parse(address=pair[0])
    else:
        # got name & address
        name = pair[0]
        address = Address.parse(address=pair[1])
    if address is not None:
        return Identifier(identifier=string, address=address, name=name, terminal=terminal)


def concat(address: Address, name: Optional[str] = None, terminal: Optional[str] = None) -> str:
    string = str(address)
    if name is not None and len(name) > 0:
        string = name + '@' + string
    if terminal is not None and len(terminal) > 0:
        string = string + '/' + terminal
    return string


class Identifier(String, ID):

    def __init__(self, identifier: str, address: Address, name: Optional[str]=None, terminal: Optional[str]=None):
        super().__init__(string=identifier)
        self.__name = name
        self.__address = address
        self.__terminal = terminal

    @property
    def name(self) -> Optional[str]:
        return self.__name

    @property
    def address(self) -> Address:
        return self.__address

    @property
    def terminal(self) -> Optional[str]:
        return self.__terminal


"""
    ID factory
    ~~~~~~~~~~
"""


class IDFactory(ID.Factory):

    def __init__(self):
        super().__init__()
        self.__ids = {}

    def create_identifier(self, address: Address, name: Optional[str]=None, terminal: Optional[str]=None) -> ID:
        identifier = concat(address=address, name=name, terminal=terminal)
        _id = self.__ids.get(identifier)
        if _id is None:
            _id = Identifier(identifier=identifier, address=address, name=name, terminal=terminal)
            self.__ids[identifier] = _id
        return _id

    def parse_identifier(self, identifier: str) -> Optional[ID]:
        _id = self.__ids.get(identifier)
        if _id is None:
            _id = parse(string=identifier)
            if _id is not None:
                self.__ids[identifier] = _id
        return _id


"""
    ID for Broadcast
    ~~~~~~~~~~~~~~~~
"""

# register ID factory
ID.register(factory=IDFactory())

ANYONE = ID.create(name='anyone', address=ANYWHERE)
EVERYONE = ID.create(name='everyone', address=EVERYWHERE)

# DIM Founder
FOUNDER = ID.create(name='moky', address=ANYWHERE)
