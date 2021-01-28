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
    Invite Group Command Processor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    1. add new member(s) to the group
    2. any member or assistant can invite new member
"""

from typing import Optional

from dimp import ID
from dimp import ReliableMessage
from dimp import Content
from dimp import Command, GroupCommand, InviteCommand

from .command import CommandProcessor
from .history import GroupCommandProcessor


class InviteCommandProcessor(GroupCommandProcessor):

    def __reset(self, cmd: Command, msg: ReliableMessage) -> Content:
        """
        Call reset command processor

        :param cmd: invite(reset) command
        :param msg: instant message
        :return: response from invite command processor
        """
        cpu = CommandProcessor.processor_for_name(command=GroupCommand.RESET)
        assert isinstance(cpu, GroupCommandProcessor), 'failed to get "reset" command processor'
        cpu.messenger = self.messenger
        return cpu.execute(cmd=cmd, msg=msg)

    def execute(self, cmd: Command, msg: ReliableMessage) -> Optional[Content]:
        assert isinstance(cmd, InviteCommand), 'group command error: %s' % cmd
        facebook = self.facebook
        from ..facebook import Facebook
        assert isinstance(facebook, Facebook), 'entity delegate error: %s' % facebook
        # 0. check group
        group = cmd.group
        owner = facebook.owner(identifier=group)
        members = facebook.members(identifier=group)
        if owner is None or members is None or len(members) == 0:
            # NOTICE: group membership lost?
            #         reset group members
            return self.__reset(cmd=cmd, msg=msg)
        # 1. check permission
        sender = msg.sender
        if sender not in members:
            # not a member? check assistants
            assistants = facebook.assistants(identifier=group)
            if assistants is None or sender not in assistants:
                raise AssertionError('only member/assistant can invite: %s' % msg)
        # 2. inviting members
        invite_list = self.members(cmd=cmd)
        if invite_list is None or len(invite_list) == 0:
            raise ValueError('invite command error: %s' % cmd)
        # 2.1. check for reset
        if sender == owner and owner in invite_list:
            # NOTICE: owner invites owner?
            #         it means this should be a 'reset' command
            return self.__reset(cmd=cmd, msg=msg)
        # 2.2. build invited-list
        add_list = []
        for item in invite_list:
            if item in members:
                continue
            # new member found
            add_list.append(item)
            members.append(item)
        # 2.3. do invite
        if len(add_list) > 0:
            if facebook.save_members(members=members, identifier=group):
                cmd['added'] = ID.revert(add_list)
        # 3. response (no need to response this group command)
        return None
