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
    Station & Service Provider (SP)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Station : DIM network server node
    SP      : DIM network service provider
"""

from dimp import NetworkType, ID, User, Group


class Station(User):

    def __init__(self, identifier: ID, host: str = None, port: int = 0):
        super().__init__(identifier=identifier)
        assert identifier.type == NetworkType.STATION, 'Station ID type error: %s' % identifier
        self.__host = host
        self.__port = port

    def __str__(self):
        clazz = self.__class__.__name__
        identifier = self.identifier
        network = identifier.address.network
        host = self.host
        port = self.port
        return '<%s: %s(%d) host="%s" port=%d />' % (clazz, identifier, network, host, port)

    @property
    def host(self) -> str:
        if self.__host is None:
            doc = self.document(doc_type='*')
            if doc is not None:
                value = doc.get_property('host')
                if value is not None:
                    self.__host = str(value)
            if self.__host is None:
                self.__host = '0.0.0.0'
        return self.__host

    @property
    def port(self) -> int:
        if self.__port == 0:
            doc = self.document(doc_type='*')
            if doc is not None:
                value = doc.get_property('port')
                if value is not None:
                    self.__port = int(value)
            if self.__port == 0:
                self.__port = 9394
        return self.__port


class ServiceProvider(Group):

    def __init__(self, identifier: ID):
        super().__init__(identifier=identifier)
        assert identifier.type == NetworkType.PROVIDER, 'Service Provider ID type error: %s' % identifier

    @property
    def stations(self):
        return self.members
