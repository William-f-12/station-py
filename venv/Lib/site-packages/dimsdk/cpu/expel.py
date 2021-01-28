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
    Expel Group Command Processor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    1. remove group member(s)
    2. only group owner or assistant can expel member
"""

from typing import Optional

from dimp import ID
from dimp import ReliableMessage
from dimp import Content
from dimp import Command, ExpelCommand

from .history import GroupCommandProcessor


class ExpelCommandProcessor(GroupCommandProcessor):

    def execute(self, cmd: Command, msg: ReliableMessage) -> Optional[Content]:
        assert isinstance(cmd, ExpelCommand), 'group command error: %s' % cmd
        facebook = self.facebook
        from ..facebook import Facebook
        assert isinstance(facebook, Facebook), 'entity delegate error: %s' % facebook
        # 0. check group
        group = cmd.group
        owner = facebook.owner(identifier=group)
        members = facebook.members(identifier=group)
        if owner is None or members is None or len(members) == 0:
            raise LookupError('Group not ready: %s' % group)
        # 1. check permission
        sender = msg.sender
        if sender != owner:
            # not the owner? check assistants
            assistants = facebook.assistants(identifier=group)
            if assistants is None or sender not in assistants:
                text = '%s is not the owner/assistant of group %s, cannot expel member' % (sender, group)
                raise AssertionError(text)
        # 2. expelling members
        expel_list = self.members(cmd=cmd)
        if expel_list is None or len(expel_list) == 0:
            raise ValueError('expel command error: %s' % cmd)
        # 2.1. check owner
        if owner in expel_list:
            raise AssertionError('cannot expel owner %s of group %s' % (owner, group))
        # 2.2. build removed-list
        remove_list = []
        for item in expel_list:
            if item not in members:
                continue
            # expelled member found
            remove_list.append(item)
            members.remove(item)
        # 2.3. do expel
        if len(remove_list) > 0:
            if facebook.save_members(members=members, identifier=group):
                cmd['removed'] = ID.revert(remove_list)
        # 3. response (no need to response this group command)
        return None
