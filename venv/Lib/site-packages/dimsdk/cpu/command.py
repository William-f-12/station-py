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
    Command Processor
    ~~~~~~~~~~~~~~~~~

"""

from typing import Optional, Union

from dimp.protocol.command import command_name
from dimp import ReliableMessage
from dimp import Content, TextContent
from dimp import Command, GroupCommand

from .content import ContentProcessor


class CommandProcessor(ContentProcessor):

    def execute(self, cmd: Command, msg: ReliableMessage) -> Optional[Content]:
        text = 'Command (name: %s) not support yet!' % cmd.command
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
        assert isinstance(content, Command), 'command error: %s' % content
        # process command by name
        cpu = self.processor_for_command(cmd=content)
        if cpu is None:
            if isinstance(content, GroupCommand):
                cpu = self.processor_for_name(command='group')
        if cpu is None:
            cpu = self
        else:
            assert isinstance(cpu, CommandProcessor), 'CPU error: %s' % cpu
            cpu.messenger = self.messenger
        return cpu.execute(cmd=content, msg=msg)

    #
    #   CPU factory
    #

    @classmethod
    def processor_for_command(cls, cmd: Union[Command, dict]):  # -> Optional[CommandProcessor]:
        if isinstance(cmd, Command):
            cmd = cmd.dictionary
        name = command_name(cmd=cmd)
        return cls.processor_for_name(command=name)

    @classmethod
    def processor_for_name(cls, command: str):  # -> Optional[CommandProcessor]:
        return cls.__command_processors.get(command)

    @classmethod
    def register(cls, command: str, cpu):
        cls.__command_processors[command] = cpu

    __command_processors = {}
