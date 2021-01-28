# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao: Universal Message Module
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

import random
import time as time_lib
from abc import abstractmethod
from typing import Optional, Union

from mkm.crypto import Map, Dictionary
from mkm import ID

from .types import ContentType


class Content(Map):
    """This class is for creating message content

        Message Content
        ~~~~~~~~~~~~~~~

        data format: {
            'type'    : 0x00,            // message type
            'sn'      : 0,               // serial number

            'group'   : 'Group ID',      // for group message

            //-- message info
            'text'    : 'text',          // for text message
            'command' : 'Command Name',  // for system command
            //...
        }
    """

    @property
    @abstractmethod
    def type(self) -> int:
        """ content type """
        raise NotImplemented

    @property
    @abstractmethod
    def serial_number(self) -> int:
        """ serial number as message id """
        raise NotImplemented

    @property
    @abstractmethod
    def time(self) -> Optional[int]:
        """ message time """
        raise NotImplemented

    @property
    @abstractmethod
    def group(self) -> Optional[ID]:
        """
            Group ID/string for group message
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if field 'group' exists, it means this is a group message
        """
        raise NotImplemented

    @group.setter
    @abstractmethod
    def group(self, value: ID):
        raise NotImplemented

    #
    #   Content factory
    #
    class Factory:

        @abstractmethod
        def parse_content(self, content: dict):  # -> Optional[Content]:
            """
            Parse map object to content

            :param content: content info
            :return: Content
            """
            raise NotImplemented

    __factories = {}  # type -> factory

    @classmethod
    def register(cls, content_type: Union[ContentType, int], factory: Factory):
        if isinstance(content_type, ContentType):
            content_type = content_type.value
        cls.__factories[content_type] = factory

    @classmethod
    def factory(cls, content_type: Union[ContentType, int]) -> Factory:
        if isinstance(content_type, ContentType):
            content_type = content_type.value
        return cls.__factories.get(content_type)

    @classmethod
    def parse(cls, content: dict):  # -> Content:
        if content is None:
            return None
        elif isinstance(content, Content):
            return content
        elif isinstance(content, Map):
            content = content.dictionary
        _type = msg_type(content=content)
        factory = cls.factory(content_type=_type)
        if factory is None:
            factory = cls.factory(content_type=0)  # unknown
            assert factory is not None, 'cannot parse content: %s' % content
        return factory.parse_content(content=content)


"""
    Implements
    ~~~~~~~~~~
"""


def msg_type(content: dict) -> int:
    return int(content.get('type'))


def msg_id(content: dict) -> int:
    return int(content.get('sn'))


def msg_time(content: dict) -> Optional[int]:
    timestamp = content.get('time')
    if timestamp is not None:
        return int(timestamp)


def content_group(content: dict) -> Optional[ID]:
    group = content.get('group')
    if group is not None:
        return ID.parse(identifier=group)


def content_set_group(content: dict, group: ID):
    if group is None:
        content.pop('group', None)
    else:
        content['group'] = str(group)


def random_positive_integer():
    """
    :return: random integer greater than 0
    """
    return random.randint(1, 2**32-1)


class BaseContent(Dictionary, Content):

    def __init__(self, content: Optional[dict]=None, content_type: Union[ContentType, int]=0):
        super().__init__(dictionary=content)
        if isinstance(content_type, ContentType):
            content_type = content_type.value
        if content_type > 0:
            self.__type = content_type
            self.__sn = random_positive_integer()
            self.__time = int(time_lib.time())
            self['type'] = self.__type
            self['sn'] = self.__sn
            self['time'] = self.__time
        else:
            assert isinstance(content, dict), 'content error: %s' % content
            # lazy load
            self.__type = 0
            self.__sn = 0
            self.__time = 0
        # group ID
        self.__group = None

    # message content type: text, image, ...
    @property
    def type(self) -> int:
        if self.__type is 0:
            self.__type = msg_type(content=self.dictionary)
        return self.__type

    # serial number: random number to identify message content
    @property
    def serial_number(self) -> int:
        if self.__sn is 0:
            self.__sn = msg_id(content=self.dictionary)
        return self.__sn

    @property
    def time(self) -> Optional[int]:
        if self.__time is 0:
            self.__time = msg_time(content=self.dictionary)
        return self.__time

    @property
    def group(self) -> Optional[ID]:
        if self.__group is None:
            self.__group = content_group(content=self.dictionary)
        return self.__group

    @group.setter
    def group(self, value: ID):
        content_set_group(content=self.dictionary, group=value)
        self.__group = value
