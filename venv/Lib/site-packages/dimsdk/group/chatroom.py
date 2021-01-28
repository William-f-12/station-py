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
    Chatroom
    ~~~~~~~~

    Big group with admins
"""

from abc import abstractmethod
from typing import Optional, List

from dimp import ID, NetworkType
from dimp import Group, GroupDataSource


class ChatroomDataSource(GroupDataSource):
    """This interface is for getting information for chatroom

        Chatroom Data Source
        ~~~~~~~~~~~~~~~~~~~~

        Chatroom admins should be set complying with the consensus algorithm
    """

    @abstractmethod
    def admins(self, identifier: ID) -> Optional[List[ID]]:
        """
        Get all admins in the chatroom

        :param identifier: chatroom ID
        :return: admin ID list
        """
        pass


class Chatroom(Group):

    def __init__(self, identifier: ID):
        super().__init__(identifier=identifier)
        assert identifier.type == NetworkType.CHATROOM, 'Chatroom ID type error: %s' % identifier

    @Group.delegate.getter
    def delegate(self) -> Optional[ChatroomDataSource]:
        facebook = super().delegate
        assert facebook is None or isinstance(facebook, ChatroomDataSource), 'error: %s' % facebook
        return facebook

    # @delegate.setter
    # def delegate(self, value: ChatroomDataSource):
    #     super(Chatroom, Chatroom).delegate.__set__(self, value)

    @property
    def admins(self) -> Optional[List[ID]]:
        return self.delegate.admins(identifier=self.identifier)
