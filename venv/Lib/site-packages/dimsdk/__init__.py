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

from .plugins import *

from .network import ServiceProvider, Station, Robot

from .group import Polylogue, Chatroom, ChatroomDataSource

from .protocol import ReceiptCommand, HandshakeCommand, LoginCommand
from .protocol import BlockCommand, MuteCommand, StorageCommand

from .cpu import ContentProcessor, ForwardContentProcessor, FileContentProcessor
from .cpu import CommandProcessor, HistoryCommandProcessor, GroupCommandProcessor
from .cpu import InviteCommandProcessor, ExpelCommandProcessor, QuitCommandProcessor
from .cpu import ResetCommandProcessor, QueryCommandProcessor
from .cpu import MetaCommandProcessor, DocumentCommandProcessor

from .delegate import Callback, CompletionHandler, MessengerDelegate, MessengerDataSource

from .facebook import Facebook
from .packer import MessagePacker
from .processor import MessageProcessor
from .transmitter import MessageTransmitter
from .messenger import Messenger

from .ans import AddressNameService

name = 'DIM-SDK'

__author__ = 'Albert Moky'

__all__ = [

    #
    #   Plugins
    #
    'PlainKey',
    'BTCAddress', 'ETHAddress',
    'DefaultMeta', 'BTCMeta', 'ETHMeta',

    #
    #   Protocol
    #
    'ReceiptCommand', 'HandshakeCommand', 'LoginCommand',
    'BlockCommand', 'MuteCommand', 'StorageCommand',

    #
    #   Content/Command Processors
    #
    'ContentProcessor', 'ForwardContentProcessor', 'FileContentProcessor',
    'CommandProcessor', 'HistoryCommandProcessor',
    'GroupCommandProcessor',
    'InviteCommandProcessor', 'ExpelCommandProcessor', 'QuitCommandProcessor',
    'ResetCommandProcessor', 'QueryCommandProcessor',
    'MetaCommandProcessor', 'DocumentCommandProcessor',

    # network
    'ServiceProvider', 'Station', 'Robot',

    # group
    'Polylogue', 'Chatroom', 'ChatroomDataSource',

    # delegate
    'Callback', 'CompletionHandler', 'MessengerDelegate', 'MessengerDataSource',

    'AddressNameService', 'Facebook',
    'Messenger', 'MessagePacker', 'MessageProcessor', 'MessageTransmitter',
]
