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
    Content Processor
    ~~~~~~~~~~~~~~~~~

"""

import weakref
from typing import Optional, Union

from dkd.content import msg_type

from dimp import ReliableMessage
from dimp import ContentType, Content, TextContent


class ContentProcessor:

    def __init__(self):
        super().__init__()
        self.__messenger: Optional[weakref.ReferenceType] = None

    @property
    def messenger(self):  # Messenger
        if self.__messenger is not None:
            return self.__messenger()

    @messenger.setter
    def messenger(self, transceiver):
        self.__messenger = weakref.ref(transceiver)

    @property
    def facebook(self):  # Facebook
        return self.messenger.facebook

    #
    #   main
    #
    def process(self, content: Content, msg: ReliableMessage) -> Optional[Content]:
        text = 'Content (type: %s) not support yet!' % content.type
        res = TextContent(text=text)
        # check group message
        group = content.group
        if group is not None:
            res.group = group
        return res

    #
    #   CPU factory
    #

    @classmethod
    def processor_for_content(cls, content: Union[Content, dict]):  # -> Optional[ContentProcessor]:
        if isinstance(content, Content):
            content = content.dictionary
        content_type = msg_type(content=content)
        return cls.processor_for_type(content_type=content_type)

    @classmethod
    def processor_for_type(cls, content_type: Union[ContentType, int]):  # -> Optional[ContentProcessor]:
        if isinstance(content_type, ContentType):
            content_type = content_type.value
        return cls.__content_processors.get(content_type)

    @classmethod
    def register(cls, content_type: Union[ContentType, int], cpu):
        if isinstance(content_type, ContentType):
            content_type = content_type.value
        cls.__content_processors[content_type] = cpu

    __content_processors = {}
