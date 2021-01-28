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
    Quit Group Command Processor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    1. quit the group
    2. owner and assistant cannot quit
    3. assistant can be hired/fired by owner
"""

from typing import Optional

from dimp import ReliableMessage
from dimp import Content
from dimp import Command, QuitCommand

from .history import GroupCommandProcessor


class QuitCommandProcessor(GroupCommandProcessor):

    def execute(self, cmd: Command, msg: ReliableMessage) -> Optional[Content]:
        assert isinstance(cmd, QuitCommand), 'group command error: %s' % cmd
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
        if sender == owner:
            raise AssertionError('owner cannot quit: %s -> %s' % (sender, group))
        assistants = facebook.assistants(identifier=group)
        if assistants is not None and sender in assistants:
            raise AssertionError('assistant cannot quit: %s -> %s' % (sender, group))
        # 2. remove sender from group members
        if sender in members:
            members.remove(sender)
            facebook.save_members(members=members, identifier=group)
        # 3. response (no need to response this group command)
        return None
