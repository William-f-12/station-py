# -*- coding: utf-8 -*-
#
#   DIM-SDK : Decentralized Instant Messaging Software Development Kit
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

"""
    Session Server
    ~~~~~~~~~~~~~~

    for login user
"""

import weakref
from abc import abstractmethod
from weakref import WeakValueDictionary
from typing import Optional, Dict, Set
import numpy
import random

from dimp import hex_encode
from dimp import ID, ReliableMessage

from libs.utils import Singleton


def generate_session_key() -> str:
    return hex_encode(bytes(numpy.random.bytes(32)))


class Session:

    class Handler:
        """ Session handler """
        @abstractmethod
        def push_message(self, msg: ReliableMessage) -> bool:
            raise NotImplemented

    def __init__(self, client_address: tuple, handler: Handler):
        super().__init__()
        self.__key = generate_session_key()
        self.__address = client_address
        self.__handler = weakref.ref(handler)
        self.__identifier = None
        self.__active = True

    def __str__(self):
        clazz = self.__class__.__name__
        return '<%s:%s %s|%s active=%d />' % (clazz, self.__key,
                                              self.__address, self.__identifier,
                                              self.__active)

    @property
    def key(self) -> str:
        return self.__key

    @property
    def client_address(self) -> tuple:
        """ (IP, port) """
        return self.__address

    @property
    def handler(self) -> Optional[Handler]:
        """ Request handler """
        return self.__handler()

    @property
    def identifier(self) -> Optional[ID]:
        return self.__identifier

    @identifier.setter
    def identifier(self, value: ID):
        self.__identifier = value

    @property
    def active(self) -> bool:
        """ when the client entered background, it should be set to False """
        return self.__active

    @active.setter
    def active(self, value: bool):
        self.__active = value

    def push_message(self, msg: ReliableMessage) -> bool:
        """ Push message when session active """
        if self.__active:
            return self.handler.push_message(msg=msg)


@Singleton
class SessionServer:

    def __init__(self):
        super().__init__()
        # memory cache
        self.__client_addresses: Dict[ID, Set[tuple]] = {}             # {identifier, [client_address]}
        self.__sessions: Dict[tuple, Session] = WeakValueDictionary()  # {client_address, session}

    def get_session(self, client_address: tuple, handler: Optional[Session.Handler]=None) -> Session:
        """ Session factory """
        session = self.__sessions.get(client_address)
        if session is None and handler is not None:
            # create a new session and cache it
            session = Session(client_address=client_address, handler=handler)
            self.__sessions[client_address] = session
        return session

    def __insert(self, client_address: tuple, identifier: ID):
        array = self.__client_addresses.get(identifier)
        if array is None:
            array = set()
            self.__client_addresses[identifier] = array
        array.add(client_address)

    def __remove(self, client_address: tuple, identifier: ID):
        array = self.__client_addresses.get(identifier)
        if array is not None:
            array.discard(client_address)
            if len(array) == 0:
                # all sessions removed
                self.__client_addresses.pop(identifier)

    def update_session(self, session: Session, identifier: ID):
        """ Insert a session with ID into memory cache """
        address = session.client_address
        assert address is not None, 'session error: %s' % session
        old = session.identifier
        if old is not None:
            # 0. remove client_address from old ID
            self.__remove(client_address=address, identifier=old)
        # 1. insert client_address for new ID
        self.__insert(client_address=address, identifier=identifier)
        # 2. update session ID
        session.identifier = identifier

    def remove_session(self, session: Session):
        """ Remove the session from memory cache """
        identifier = session.identifier
        address = session.client_address
        assert address is not None, 'session error: %s' % session
        if identifier is not None:
            # 1. remove client_address with ID
            self.__remove(client_address=address, identifier=identifier)
        # 2. remove session with client_address
        session.active = False
        self.__sessions.pop(address, None)

    def all_sessions(self, identifier: ID) -> Set[Session]:
        """ Get all sessions of this user """
        results = set()
        # 1. get all client_address with ID
        array = self.__client_addresses.get(identifier)
        if array is not None:
            array = array.copy()
            # 2. get session by each client_address
            for item in array:
                session = self.__sessions.get(item)
                if session is not None:
                    results.add(session)
        return results

    def active_sessions(self, identifier: ID) -> Set[Session]:
        results = set()
        # 1. get all sessions
        array = self.all_sessions(identifier=identifier)
        for item in array:
            # 2. check session active
            if item.active:
                results.add(item)
        return results

    #
    #   Users
    #
    def all_users(self) -> Set[ID]:
        """ Get all users """
        return set(self.__client_addresses.keys())

    def is_active(self, identifier: ID) -> bool:
        """ Check whether user has active session """
        sessions = self.all_sessions(identifier=identifier)
        for item in sessions:
            if item.active:
                return True

    def active_users(self) -> Set[ID]:
        """ Get active users """
        users = set()
        array = self.all_users()
        for item in array:
            if self.is_active(identifier=item):
                users.add(item)
        return users

    def random_users(self, max_count=20) -> Set[ID]:
        array = self.active_users()
        count = len(array)
        if count > 1:
            # limit the response
            if count > max_count:
                count = max_count
            some = random.sample(array, count)
            array = set(some)
        return array
