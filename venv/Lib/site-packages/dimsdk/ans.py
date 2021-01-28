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
    Address Name Service
    ~~~~~~~~~~~~~~~~~~~~

    A map for short name to ID, just like DNS
"""

from abc import ABC, abstractmethod
from typing import Optional, List

from dimp import ID, ANYONE, EVERYONE, FOUNDER

#
#   Reserved names
#
keywords = [
    "all", "everyone", "anyone", "owner", "founder",
    # --------------------------------
    "dkd", "mkm", "dimp", "dim", "dimt",
    "rsa", "ecc", "aes", "des", "btc", "eth",
    # --------------------------------
    "crypto", "key", "symmetric", "asymmetric",
    "public", "private", "secret", "password",
    "id", "address", "meta",
    "tai", "document", "profile", "visa", "bulletin",
    "entity", "user", "group", "contact",
    # --------------------------------
    "member", "admin", "administrator", "assistant",
    "main", "polylogue", "chatroom",
    "social", "organization",
    "company", "school", "government", "department",
    "provider", "station", "thing", "robot",
    # --------------------------------
    "message", "instant", "secure", "reliable",
    "envelope", "sender", "receiver", "time",
    "content", "forward", "command", "history",
    "keys", "data", "signature",
    # --------------------------------
    "type", "serial", "sn",
    "text", "file", "image", "audio", "video", "page",
    "handshake", "receipt", "block", "mute",
    "register", "suicide", "found", "abdicate",
    "invite", "expel", "join", "quit", "reset", "query",
    "hire", "fire", "resign",
    # --------------------------------
    "server", "client", "terminal", "local", "remote",
    "barrack", "cache", "transceiver",
    "ans", "facebook", "store", "messenger",
    "root", "supervisor",
]


class AddressNameService(ABC):

    def __init__(self):
        super().__init__()
        # ANS records
        self.__caches = {
            'all': EVERYONE,
            'everyone': EVERYONE,
            'anyone': ANYONE,
            'owner': ANYONE,
            'founder': FOUNDER,
        }

    @staticmethod
    def is_reserved(name: str) -> bool:
        return name in keywords

    def cache(self, name: str, identifier: ID = None) -> bool:
        if self.is_reserved(name):
            # this name is reserved, cannot register
            return False
        if identifier is None:
            self.__caches.pop(name, None)
        else:
            self.__caches[name] = identifier
        return True

    def identifier(self, name: str) -> Optional[ID]:
        """ Get ID by short name """
        return self.__caches.get(name)

    def names(self, identifier: ID) -> Optional[List[str]]:
        """ Get all short names with the same ID """
        array = []
        for (key, value) in self.__caches.items():
            if key == identifier:
                array.append(value)
        return array

    @abstractmethod
    def save(self, name: str, identifier: ID = None) -> bool:
        """
        Save ANS record

        :param name:       username
        :param identifier: user ID; if empty, means delete this name
        :return: True on success
        """
        if not self.cache(name=name, identifier=identifier):
            return False
