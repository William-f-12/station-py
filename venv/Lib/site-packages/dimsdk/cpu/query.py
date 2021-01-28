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
    Query Group Command Processor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    1. query for group members-list
    2. any existed member or assistant can query group members-list
"""

from typing import Optional

from dimp import ReliableMessage
from dimp import Content, TextContent
from dimp import Command, GroupCommand, QueryCommand

from .history import GroupCommandProcessor


class QueryCommandProcessor(GroupCommandProcessor):

    def execute(self, cmd: Command, msg: ReliableMessage) -> Optional[Content]:
        assert isinstance(cmd, QueryCommand), 'group command error: %s' % cmd
        facebook = self.facebook
        from ..facebook import Facebook
        assert isinstance(facebook, Facebook), 'entity delegate error: %s' % facebook
        # 0. check group
        group = cmd.group
        owner = facebook.owner(identifier=group)
        members = facebook.members(identifier=group)
        if owner is None or members is None or len(members) == 0:
            text = 'Sorry, members not found in group: %s' % group
            res = TextContent(text=text)
            res.group = group
            return res
        # 1. check permission
        sender = msg.sender
        if sender not in members:
            # not a member? check assistants
            assistants = facebook.assistants(identifier=group)
            if assistants is None or sender not in assistants:
                text = '%s is not a member/assistant of group %s, cannot query.' % (sender, group)
                raise AssertionError(text)
        # 2. respond
        user = facebook.current_user
        assert user is not None, 'current user not set'
        if user.identifier == owner:
            return GroupCommand.reset(group=group, members=members)
        else:
            return GroupCommand.invite(group=group, members=members)
