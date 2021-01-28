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
    Content/Command Processing Units
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from dimp import *

from .content import ContentProcessor
from .forward import ForwardContentProcessor
from .file import FileContentProcessor

from .command import CommandProcessor
from .history import HistoryCommandProcessor, GroupCommandProcessor
from .invite import InviteCommandProcessor
from .expel import ExpelCommandProcessor
from .quit import QuitCommandProcessor
from .reset import ResetCommandProcessor
from .query import QueryCommandProcessor

from .meta import MetaCommandProcessor
from .document import DocumentCommandProcessor


def register_content_processors():
    ContentProcessor.register(content_type=ContentType.FORWARD, cpu=ForwardContentProcessor())
    # files
    fpu = FileContentProcessor()
    ContentProcessor.register(content_type=ContentType.FILE, cpu=fpu)
    ContentProcessor.register(content_type=ContentType.IMAGE, cpu=fpu)
    ContentProcessor.register(content_type=ContentType.AUDIO, cpu=fpu)
    ContentProcessor.register(content_type=ContentType.VIDEO, cpu=fpu)
    # commands
    ContentProcessor.register(content_type=ContentType.COMMAND, cpu=CommandProcessor())
    ContentProcessor.register(content_type=ContentType.HISTORY, cpu=HistoryCommandProcessor())
    # default
    ContentProcessor.register(content_type=0, cpu=ContentProcessor())


def register_command_processors():
    # meta
    CommandProcessor.register(command=Command.META, cpu=MetaCommandProcessor())
    # document
    dpu = DocumentCommandProcessor()
    CommandProcessor.register(command=Command.DOCUMENT, cpu=dpu)
    CommandProcessor.register(command='profile', cpu=dpu)
    CommandProcessor.register(command='visa', cpu=dpu)
    CommandProcessor.register(command='bulletin', cpu=dpu)
    # group commands
    CommandProcessor.register(command='group', cpu=GroupCommandProcessor())
    CommandProcessor.register(command=GroupCommand.INVITE, cpu=InviteCommandProcessor())
    CommandProcessor.register(command=GroupCommand.EXPEL, cpu=ExpelCommandProcessor())
    CommandProcessor.register(command=GroupCommand.QUIT, cpu=QuitCommandProcessor())
    CommandProcessor.register(command=GroupCommand.QUERY, cpu=QueryCommandProcessor())
    CommandProcessor.register(command=GroupCommand.RESET, cpu=ResetCommandProcessor())


register_content_processors()
register_command_processors()


__all__ = [

    'ContentProcessor',
    'ForwardContentProcessor',
    'FileContentProcessor',

    'CommandProcessor',
    'HistoryCommandProcessor',

    'GroupCommandProcessor',
    'InviteCommandProcessor', 'ExpelCommandProcessor', 'QuitCommandProcessor',
    'ResetCommandProcessor', 'QueryCommandProcessor',

    'MetaCommandProcessor',
    'DocumentCommandProcessor',
]
