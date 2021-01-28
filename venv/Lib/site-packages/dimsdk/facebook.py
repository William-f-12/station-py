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
    Facebook
    ~~~~~~~~

    Barrack for cache entities
"""

from abc import abstractmethod
from typing import Optional, List

from dimp import NetworkType, ID
from dimp import User, Group
from dimp import Meta, Document
from dimp import Barrack

from .network import ServiceProvider, Station, Robot
from .group import Polylogue


class Facebook(Barrack):

    @property
    def current_user(self) -> Optional[User]:
        """
        Get current user (for signing and sending message)

        :return: User
        """
        users = self.local_users
        if users is not None and len(users) > 0:
            return users[0]

    @abstractmethod
    def save_meta(self, meta: Meta, identifier: ID) -> bool:
        """
        Save meta for entity ID (must verify first)

        :param meta:       entity meta
        :param identifier: entity ID
        :return: True on success
        """
        raise NotImplemented

    @abstractmethod
    def save_document(self, document: Document) -> bool:
        """
        Save entity document with ID (must verify first)

        :param document: entity document
        :return: True on success
        """
        raise NotImplemented

    #
    #   Group Members
    #
    @abstractmethod
    def save_members(self, members: List[ID], identifier: ID) -> bool:
        """
        Save members of group

        :param members:    member ID list
        :param identifier: group ID
        :return: True on success
        """
        raise NotImplemented

    #
    #   Document checking
    #
    @staticmethod
    def is_empty_document(document: Document) -> bool:
        if document is None:
            return True
        json = document.get('data')
        return json is None or len(json) == 0

    def is_valid_document(self, document: Document) -> bool:
        identifier = document.identifier
        if identifier is None:
            return False
        # NOTICE: if this is a group profile,
        #             verify it with each member's meta.key
        #         else (this is a user profile)
        #             verify it with the user's meta.key
        if identifier.is_group:
            # check by each member
            members = self.members(identifier=identifier)
            if members is not None:
                for item in members:
                    meta = self.meta(identifier=item)
                    if meta is None:
                        # FIXME: meta not found for this member
                        continue
                    if document.verify(public_key=meta.key):
                        return True
            # DISCUSS: what to do about assistants?

            # check by owner
            owner = self.owner(identifier=identifier)
            if owner is None:
                if identifier.type == NetworkType.POLYLOGUE:
                    # NOTICE: if this is a polylogue profile
                    #             verify it with the founder's meta.key
                    #             (which equals to the group's meta.key)
                    meta = self.meta(identifier=identifier)
                else:
                    # FIXME: owner not found for this group
                    return False
            elif owner in members:
                # already checked
                return False
            else:
                meta = self.meta(identifier=owner)
        else:
            meta = self.meta(identifier=identifier)
        if meta is not None:
            return document.verify(public_key=meta.key)

    def create_user(self, identifier: ID) -> Optional[User]:
        if identifier.is_broadcast:
            # create user 'anyone@anywhere'
            return User(identifier=identifier)
        # make sure meta exists
        assert self.meta(identifier) is not None, 'failed to get meta for user: %s' % identifier
        # TODO: make sure visa key exists before calling this
        # check user type
        u_type = identifier.type
        if u_type in [NetworkType.MAIN, NetworkType.BTC_MAIN]:
            return User(identifier=identifier)
        if u_type == NetworkType.ROBOT:
            return Robot(identifier=identifier)
        if u_type == NetworkType.STATION:
            return Station(identifier=identifier)
        raise TypeError('unsupported user type: %s' % u_type)

    def create_group(self, identifier: ID) -> Optional[Group]:
        if identifier.is_broadcast:
            # create group 'everyone@everywhere'
            return Group(identifier=identifier)
        # make sure meta exists
        assert self.meta(identifier) is not None, 'failed to get meta for group: %s' % identifier
        # check group type
        g_type = identifier.type
        if g_type == NetworkType.POLYLOGUE:
            return Polylogue(identifier=identifier)
        if g_type == NetworkType.CHATROOM:
            raise NotImplementedError('Chatroom not implemented')
        if g_type == NetworkType.PROVIDER:
            return ServiceProvider(identifier=identifier)
        raise TypeError('unsupported group type: %s' % g_type)

    # group membership

    def is_founder(self, member: ID, group: ID) -> bool:
        g_meta = self.meta(identifier=group)
        assert g_meta is not None, 'failed to get meta for group: %s' % group
        u_meta = self.meta(identifier=member)
        assert u_meta is not None, 'failed to get meta for member: %s' % member
        return g_meta.match_key(key=u_meta.key)

    def is_owner(self, member: ID, group: ID) -> bool:
        if group.type == NetworkType.POLYLOGUE:
            return self.is_founder(member=member, group=group)
        raise AssertionError('only Polylogue so far')
