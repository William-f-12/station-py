# -*- coding: utf-8 -*-
#
#   DIM-SDK : Decentralized Instant Messaging Software Development Kit
#
#                                Written in 2020 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2020 Albert Moky
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
from typing import Optional

from dimp import InstantMessage, ReliableMessage
from dimp import Content
from dimp import Processor

from .cpu import ContentProcessor
from .messenger import Messenger


class MessageProcessor(Processor):

    def __init__(self, messenger: Messenger):
        super().__init__(transceiver=messenger)

    @property
    def messenger(self) -> Messenger:
        transceiver = self.transceiver
        assert isinstance(transceiver, Messenger), 'messenger error: %s' % transceiver
        return transceiver

    def process_instant_message(self, msg: InstantMessage, r_msg: ReliableMessage) -> Optional[InstantMessage]:
        res = super().process_instant_message(msg=msg, r_msg=r_msg)
        if self.messenger.save_message(msg=msg):
            return res

    def process_content(self, content: Content, r_msg: ReliableMessage) -> Optional[Content]:
        # TODO: override to check group
        cpu = ContentProcessor.processor_for_content(content=content)
        if cpu is None:
            cpu = ContentProcessor.processor_for_type(content_type=0)  # unknown
            assert isinstance(cpu, ContentProcessor), 'cannot process content: %s' % content
        cpu.messenger = self.messenger
        return cpu.process(content=content, msg=r_msg)
        # TODO: override to filter the response
