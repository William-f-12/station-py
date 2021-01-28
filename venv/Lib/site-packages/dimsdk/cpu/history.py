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
    Group History Processors
    ~~~~~~~~~~~~~~~~~~~~~~~~

"""

from typing import Optional, List

from dimp import ID, ReliableMessage
from dimp import Content, TextContent
from dimp import Command, GroupCommand

from .content import ContentProcessor
from .command import CommandProcessor


class HistoryCommandProcessor(CommandProcessor):

    def execute(self, cmd: Command, msg: ReliableMessage) -> Optional[Content]:
        text = 'History command (name: %s) not support yet!' % cmd.command
        res = TextContent(text=text)
        # check group message
        group = cmd.group
        if group is not None:
            res.group = group
        return res


class GroupCommandProcessor(HistoryCommandProcessor):

    @staticmethod
    def members(cmd: GroupCommand) -> Optional[List[ID]]:
        # get from 'members'
        array = cmd.members
        if array is None:
            # get from 'member
            item = cmd.member
            if item is not None:
                array = [item]
        return array

    def execute(self, cmd: Command, msg: ReliableMessage) -> Optional[Content]:
        text = 'Group command (name: %s) not support yet!' % cmd.command
        res = TextContent(text=text)
        # check group message
        group = cmd.group
        if group is not None:
            res.group = group
        return res

    #
    #   main
    #
    def process(self, content: Content, msg: ReliableMessage) -> Optional[Content]:
        assert isinstance(content, GroupCommand), 'group cmd error: %s' % content
        # process command by name
        cpu = CommandProcessor.processor_for_command(cmd=content)
        if cpu is None:
            cpu = self
        else:
            assert isinstance(cpu, ContentProcessor), 'CPU error: %s' % cpu
            cpu.messenger = self.messenger
        return cpu.execute(cmd=content, msg=msg)
