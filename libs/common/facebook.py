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

"""
    Facebook
    ~~~~~~~~

    Barrack for cache entities
"""

from typing import Optional

from mkm.immortals import Immortals

from dimp import PrivateKey
from dimp import ID, Meta, Profile, User, LocalUser
from dimsdk import Facebook as Barrack

from .database import Database


class Facebook(Barrack):

    def __init__(self):
        super().__init__()
        self.database: Database = None
        # built-in accounts
        #     Immortal Hulk: 'hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj'
        #     Monkey King:   'moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk'
        self.__immortals = Immortals()

    def nickname(self, identifier: ID) -> str:
        assert identifier.type.is_user(), 'ID error: %s' % identifier
        user = self.user(identifier=identifier)
        if user is not None:
            return user.name

    def group_name(self, identifier: ID) -> str:
        assert identifier.type.is_group(), 'ID error: %s' % identifier
        group = self.group(identifier=identifier)
        if group is None:
            return identifier.name
        else:
            return group.name

    #
    #   super()
    #
    def save_meta(self, meta: Meta, identifier: ID) -> bool:
        if not super().save_meta(meta=meta, identifier=identifier):
            # meta not match
            return False
        return self.database.save_meta(meta=meta, identifier=identifier)

    def load_meta(self, identifier: ID) -> Optional[Meta]:
        meta = super().load_meta(identifier=identifier)
        if meta is not None:
            # meta exists in cache
            return meta
        return self.database.meta(identifier=identifier)

    def save_profile(self, profile: Profile, identifier: ID=None) -> bool:
        if not super().save_profile(profile=profile, identifier=identifier):
            # profile error
            return False
        return self.database.save_profile(profile=profile)

    def load_profile(self, identifier: ID) -> Optional[Profile]:
        # profile = super().load_profile(identifier=identifier)
        # if profile is not None:
        #     # profile exists in cache
        #     return profile
        return self.database.profile(identifier=identifier)

    def save_private_key(self, key: PrivateKey, identifier: ID) -> bool:
        if not super().save_private_key(key=key, identifier=identifier):
            # key is None
            return False
        return self.database.save_private_key(private_key=key, identifier=identifier)

    def load_private_key(self, identifier: ID) -> Optional[PrivateKey]:
        key = super().load_private_key(identifier=identifier)
        if key is not None:
            # private key exists in cache
            return key
        return self.database.private_key(identifier=identifier)

    def save_contacts(self, contacts: list, identifier: ID) -> bool:
        if not super().save_contacts(contacts=contacts, identifier=identifier):
            # contacts is None (not empty list)
            return False
        return self.database.save_contacts(contacts=contacts, user=identifier)

    def load_contacts(self, identifier: ID) -> Optional[list]:
        # contacts = super().load_contacts(identifier=identifier)
        # if contacts is not None:
        #     # contacts exists in cache
        #     return contacts
        return self.database.contacts(user=identifier)

    def save_members(self, members: list, identifier: ID) -> bool:
        if not super().save_members(members=members, identifier=identifier):
            # members is None (not empty list)
            return False
        return self.database.save_members(members=members, group=identifier)

    def load_members(self, identifier: ID) -> Optional[list]:
        # members = super().load_members(identifier=identifier)
        # if members is not None:
        #     # members exists in cache
        #     return members
        return self.database.members(group=identifier)

    def save_assistants(self, assistants: list, identifier: ID) -> bool:
        # if not super().save_assistants(assistants=assistants, identifier=identifier):
        #     # assistants is None (not empty list)
        #     return False
        return True

    def load_assistants(self, identifier: ID) -> Optional[list]:
        # assistants = super().load_assistants(identifier=identifier)
        # if assistants is not None:
        #     # assistants exists in cache
        #     return assistants
        robot = self.ans.identifier(name='assistant')
        if robot is not None:
            return [robot]

    #
    #   SocialNetworkDataSource
    #
    def identifier(self, string: str) -> Optional[ID]:
        if string is None:
            return None
        if isinstance(string, ID):
            return string
        obj = self.__immortals.identifier(string=string)
        if obj is not None:
            return obj
        return super().identifier(string=string)

    def user(self, identifier: ID) -> Optional[User]:
        obj = self.__immortals.user(identifier=identifier)
        if obj is not None:
            return obj
        try:
            return super().user(identifier=identifier)
        except NotImplementedError:
            if identifier.type.is_robot():
                return self.__robot(identifier=identifier)

    def __robot(self, identifier: ID) -> Optional[User]:
        private_key = self.private_key_for_signature(identifier=identifier)
        if private_key is None:
            user = User(identifier=identifier)
        else:
            user = LocalUser(identifier=identifier)
        # cache it in barrack
        self.cache_user(user=user)
        return user

    #
    #   EntityDataSource
    #
    def meta(self, identifier: ID) -> Optional[Meta]:
        obj = self.__immortals.meta(identifier=identifier)
        if obj is not None:
            return obj
        return super().meta(identifier=identifier)

    def profile(self, identifier: ID) -> Optional[Profile]:
        obj = self.__immortals.profile(identifier=identifier)
        if obj is not None:
            return obj
        return super().profile(identifier=identifier)

    #
    #   UserDataSource
    #
    def private_key_for_signature(self, identifier: ID) -> Optional[PrivateKey]:
        obj = self.__immortals.private_key_for_signature(identifier=identifier)
        if obj is not None:
            return obj
        return super().private_key_for_signature(identifier=identifier)

    def private_keys_for_decryption(self, identifier: ID) -> Optional[list]:
        arr = self.__immortals.private_keys_for_decryption(identifier=identifier)
        if arr is not None:
            return arr
        return super().private_keys_for_decryption(identifier=identifier)

    def contacts(self, identifier: ID) -> Optional[list]:
        arr = self.__immortals.contacts(identifier=identifier)
        if arr is not None:
            return arr
        return super().contacts(identifier=identifier)

    #
    #    IGroupDataSource
    #
    def founder(self, identifier: ID) -> ID:
        # get from database
        user = self.database.founder(group=identifier)
        if user is not None:
            return user
        return super().founder(identifier=identifier)

    def owner(self, identifier: ID) -> ID:
        # get from database
        user = self.database.owner(group=identifier)
        if user is not None:
            return user
        return super().owner(identifier=identifier)
