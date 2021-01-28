# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
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
    Receipt Protocol
    ~~~~~~~~~~~~~~~~

    As receipt returned to sender to proofing the message's received
"""

from typing import Optional

from dimp import Envelope
from dimp import Command


class ReceiptCommand(Command):
    """
        Receipt Command
        ~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            command  : "receipt", // command name
            message  : "...",
            //-- extra info
            sender   : "...",
            receiver : "...",
            time     : 0
        }
    """

    def __init__(self, cmd: Optional[dict] = None,
                 envelope: Optional[Envelope] = None, message: Optional[str] = None, sn: Optional[int] = 0):
        if cmd is None:
            super().__init__(command=Command.RECEIPT)
        else:
            super().__init__(cmd=cmd)
        self.__envelope = envelope
        if envelope is not None:
            self['envelope'] = envelope.dictionary
        if message is not None:
            self['message'] = message
        if sn > 0:
            self['sn'] = sn

    # -------- setters/getters

    @property
    def message(self) -> Optional[str]:
        return self.get('message')

    @property
    def envelope(self) -> Optional[Envelope]:
        if self.__envelope is None:
            # envelope: { sender: "...", receiver: "...", time: 0 }
            env = self.get('envelope')
            if env is None and 'sender' in self and 'receiver' in self:
                env = self.dictionary
            if env is not None:
                self.__envelope = Envelope.parse(envelope=env)
        return self.__envelope
