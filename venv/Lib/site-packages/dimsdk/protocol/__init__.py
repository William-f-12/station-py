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

from dimp.protocol import register_core_factories
from dimp.protocol import Command, CommandFactoryBuilder

from .receipt import ReceiptCommand
from .handshake import HandshakeCommand
from .login import LoginCommand

from .block import BlockCommand
from .mute import MuteCommand
from .storage import StorageCommand


def register_all_factories():
    # Register core factories
    register_core_factories()

    # Register command factories
    Command.register(command=Command.RECEIPT, factory=CommandFactoryBuilder(command_class=ReceiptCommand))
    Command.register(command=Command.HANDSHAKE, factory=CommandFactoryBuilder(command_class=HandshakeCommand))
    Command.register(command=Command.LOGIN, factory=CommandFactoryBuilder(command_class=LoginCommand))

    Command.register(command=MuteCommand.MUTE, factory=CommandFactoryBuilder(command_class=MuteCommand))
    Command.register(command=BlockCommand.BLOCK, factory=CommandFactoryBuilder(command_class=BlockCommand))

    # storage (contacts, private_key)
    factory = CommandFactoryBuilder(command_class=StorageCommand)
    Command.register(command=StorageCommand.STORAGE, factory=factory)
    Command.register(command=StorageCommand.CONTACTS, factory=factory)
    Command.register(command=StorageCommand.PRIVATE_KEY, factory=factory)


register_all_factories()


__all__ = [

    'ReceiptCommand', 'HandshakeCommand', 'LoginCommand',

    'BlockCommand', 'MuteCommand', 'StorageCommand',
]
