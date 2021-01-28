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
    Forward Content Processor
    ~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from typing import Optional

from dimp import ReliableMessage
from dimp import Content, ForwardContent

from .content import ContentProcessor


#
#   Forward Content Processor
#
class ForwardContentProcessor(ContentProcessor):

    #
    #   main
    #
    def process(self, content: Content, msg: ReliableMessage) -> Optional[Content]:
        assert isinstance(content, ForwardContent), 'forward content error: %s' % content
        # call messenger to process it
        messenger = self.messenger
        # from ..messenger import Messenger
        # assert isinstance(messenger, Messenger)
        secret = content.message
        secret = messenger.process_reliable_message(msg=secret)
        # check response
        if secret is not None:
            # Over The Top
            return ForwardContent(message=secret)
        # else:
        #     receiver = content.message.receiver
        #     text = 'Message forwarded: %s' % receiver
        #     return ReceiptCommand.new(message=text)

        # NOTICE: decrypt failed, not for you?
        #         it means you are asked to re-pack and forward this message
        return None
