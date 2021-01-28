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
    Reset Group Command Processor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    1. reset group members
    2. only group owner or assistant can reset group members

    3. specially, if the group members info lost,
       means you may not known who's the group owner immediately (and he may be not online),
       so we accept the new members-list temporary, and find out who is the owner,
       after that, we will send 'query' to the owner to get the newest members-list.
"""

from typing import Optional

from dimp import ID
from dimp import ReliableMessage
from dimp import Content
from dimp import Command, GroupCommand, InviteCommand, ResetCommand

from .history import GroupCommandProcessor


class ResetCommandProcessor(GroupCommandProcessor):

    def __temporary_save(self, cmd: GroupCommand, sender: ID) -> Optional[Content]:
        facebook = self.facebook
        from ..facebook import Facebook
        assert isinstance(facebook, Facebook), 'entity delegate error: %s' % facebook
        # check whether the owner contained in the new members
        group = cmd.group
        new_members = self.members(cmd=cmd)
        if new_members is None or len(new_members) == 0:
            raise ValueError('group command error: %s' % cmd)
        for item in new_members:
            if facebook.meta(identifier=item) is None:
                # TODO: waiting for member's meta?
                continue
            if facebook.is_owner(member=item, group=group):
                # it's a full list, save it now
                if facebook.save_members(members=new_members, identifier=group):
                    if item != sender:
                        # NOTICE: to prevent counterfeit,
                        #         query the owner for newest member-list
                        cmd = GroupCommand.query(group=group)
                        messenger = self.messenger
                        from dimsdk import Messenger
                        assert isinstance(messenger, Messenger), 'message delegate error: %s' % messenger
                        messenger.send_content(sender=None, receiver=item, content=cmd, priority=1)
                # response (no need to respond this group command)
                return None
        # NOTICE: this is a partial member-list
        #         query the sender for full-list
        return GroupCommand.query(group=group)

    def execute(self, cmd: Command, msg: ReliableMessage) -> Optional[Content]:
        assert isinstance(cmd, InviteCommand) or isinstance(cmd, ResetCommand), 'group command error: %s' % cmd
        facebook = self.facebook
        from ..facebook import Facebook
        assert isinstance(facebook, Facebook), 'entity delegate error: %s' % facebook
        # 0. check group
        group = cmd.group
        owner = facebook.owner(identifier=group)
        members = facebook.members(identifier=group)
        if owner is None or members is None or len(members) == 0:
            # FIXME: group profile lost?
            # FIXME: how to avoid strangers impersonating group members?
            return self.__temporary_save(cmd=cmd, sender=msg.sender)
        # 1. check permission
        sender = msg.sender
        if sender != owner:
            # not the owner? check assistants
            assistants = facebook.assistants(identifier=group)
            if assistants is None or sender not in assistants:
                text = '%s is not the owner/assistant of group %s, cannot reset members' % (sender, group)
                raise AssertionError(text)
        # 2. resetting members
        new_members = self.members(cmd=cmd)
        if new_members is None or len(new_members) == 0:
            raise ValueError('group command error: %s' % cmd)
        # 2.1. check owner
        if owner not in new_members:
            raise AssertionError('cannot expel owner (%s) of group: %s' % (owner, group))
        # 2.2. build expelled-list
        remove_list = []
        for item in members:
            if item not in new_members:
                # removing member found
                remove_list.append(item)
        # 2.3. build invited-list
        add_list = []
        for item in new_members:
            if item not in members:
                # adding member found
                add_list.append(item)
        # 2.4. do reset
        if len(add_list) > 0 or len(remove_list) > 0:
            if facebook.save_members(members=new_members, identifier=group):
                if len(add_list) > 0:
                    cmd['added'] = ID.revert(add_list)
                if len(remove_list) > 0:
                    cmd['removed'] = ID.revert(remove_list)
        # 3. response (no need to response this group command)
        return None
