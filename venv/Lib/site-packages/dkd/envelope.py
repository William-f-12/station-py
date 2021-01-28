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

import time as time_lib
from abc import abstractmethod
from typing import Optional, Union

from mkm.crypto import Map, Dictionary
from mkm import ID

from .types import ContentType


class Envelope(Map):
    """This class is used to create a message envelope
    which contains 'sender', 'receiver' and 'time'

        Envelope for message
        ~~~~~~~~~~~~~~~~~~~~

        data format: {
            sender   : "moki@xxx",
            receiver : "hulk@yyy",
            time     : 123
        }
    """

    @property
    @abstractmethod
    def sender(self) -> ID:
        """
        Get message sender

        :return: sender ID
        """
        raise NotImplemented

    @property
    @abstractmethod
    def receiver(self) -> ID:
        """
        Get message receiver

        :return: receiver ID
        """
        raise NotImplemented

    @property
    @abstractmethod
    def time(self) -> int:
        """
        Get message time

        :return: timestamp
        """
        raise NotImplemented

    @property
    @abstractmethod
    def group(self) -> Optional[ID]:
        """
            Group ID
            ~~~~~~~~
            when a group message was split/trimmed to a single message
            the 'receiver' will be changed to a member ID, and
            the group ID will be saved as 'group'.
        """
        raise NotImplemented

    @group.setter
    @abstractmethod
    def group(self, value: ID):
        raise NotImplemented

    @property
    @abstractmethod
    def type(self) -> Optional[int]:
        """
            Message Type
            ~~~~~~~~~~~~
            because the message content will be encrypted, so
            the intermediate nodes(station) cannot recognize what kind of it.
            we pick out the content type and set it in envelope
            to let the station do its job.
        """
        raise NotImplemented

    @type.setter
    @abstractmethod
    def type(self, value: Union[ContentType, int]):
        raise NotImplemented

    #
    #   Envelope factory
    #
    class Factory:

        @abstractmethod
        def create_envelope(self, sender: ID, receiver: ID, time: int=0):  # -> Envelope:
            """
            Create envelope

            :param sender:   sender ID
            :param receiver: receiver ID
            :param time:     message time
            :return: Envelope
            """
            raise NotImplemented

        @abstractmethod
        def parse_envelope(self, envelope: dict):  # -> Optional[Envelope]:
            """
            Parse map object to envelope

            :param envelope: message head info
            :return: Envelope
            """
            raise NotImplemented

    __factory = None

    @classmethod
    def register(cls, factory: Factory):
        cls.__factory = factory

    @classmethod
    def factory(cls) -> Factory:
        return cls.__factory

    @classmethod
    def create(cls, sender: ID, receiver: ID, time: int=0):  # -> Envelope:
        factory = cls.factory()
        assert factory is not None, 'envelope factory not ready'
        return factory.create_envelope(sender=sender, receiver=receiver, time=time)

    @classmethod
    def parse(cls, envelope: dict):  # -> Envelope:
        if envelope is None:
            return None
        elif isinstance(envelope, Envelope):
            return envelope
        elif isinstance(envelope, Map):
            envelope = envelope.dictionary
        factory = cls.factory()
        assert factory is not None, 'envelope factory not ready'
        return factory.parse_envelope(envelope=envelope)


"""
    Implements
    ~~~~~~~~~~
"""


def envelope_sender(envelope: dict) -> ID:
    return ID.parse(identifier=envelope.get('sender'))


def envelope_receiver(envelope: dict) -> ID:
    return ID.parse(identifier=envelope.get('receiver'))


def envelope_time(envelope: dict) -> int:
    timestamp = envelope.get('time')
    if timestamp is None:
        return 0
    else:
        return int(timestamp)


def envelope_group(envelope: dict) -> Optional[ID]:
    group = envelope.get('group')
    if group is not None:
        return ID.parse(identifier=group)


def envelope_set_group(envelope: dict, group: ID):
    if group is None:
        envelope.pop('group', None)
    else:
        envelope['group'] = str(group)


def envelope_type(envelope: dict) -> Optional[int]:
    _type = envelope.get('type')
    if _type is not None:
        return int(_type)


def envelope_set_type(envelope: dict, content_type: Union[ContentType, int]):
    if isinstance(content_type, ContentType):
        content_type = content_type.value
    if content_type is 0:
        envelope.pop('type', None)
    else:
        envelope['type'] = content_type


class MessageEnvelope(Dictionary, Envelope):

    def __init__(self, envelope: Optional[dict]=None,
                 sender: Optional[ID]=None, receiver: Optional[ID]=None, time: Optional[int]=0):
        super().__init__(dictionary=envelope)
        # pre-process
        if envelope is None and time is 0:
            time = int(time_lib.time())
        # set values
        self.__sender = sender
        self.__receiver = receiver
        self.__time = time
        self.__group = None
        self.__type = 0
        # set values to inner dictionary
        if sender is not None:
            self['sender'] = str(sender)
        if receiver is not None:
            self['receiver'] = str(receiver)
        if time > 0:
            self['time'] = time

    @property
    def sender(self) -> ID:
        if self.__sender is None:
            self.__sender = envelope_sender(envelope=self.dictionary)
        return self.__sender

    @property
    def receiver(self) -> ID:
        if self.__receiver is None:
            self.__receiver = envelope_receiver(envelope=self.dictionary)
        return self.__receiver

    @property
    def time(self) -> int:
        if self.__time is 0:
            self.__time = envelope_time(envelope=self.dictionary)
        return self.__time

    @property
    def group(self) -> Optional[ID]:
        if self.__group is None:
            self.__group = envelope_group(envelope=self.dictionary)
        return self.__group

    @group.setter
    def group(self, value: ID):
        envelope_set_group(envelope=self.dictionary, group=value)
        self.__group = value

    @property
    def type(self) -> Optional[int]:
        if self.__type is 0:
            self.__type = envelope_type(envelope=self.dictionary)
        return self.__type

    @type.setter
    def type(self, value: Union[ContentType, int]):
        envelope_set_type(envelope=self.dictionary, content_type=value)
        self.__type = value


"""
    Envelope Factory
    ~~~~~~~~~~~~~~~~
"""


class EnvelopeFactory(Envelope.Factory):

    def create_envelope(self, sender: ID, receiver: ID, time: int=0) -> Envelope:
        return MessageEnvelope(sender=sender, receiver=receiver, time=time)

    def parse_envelope(self, envelope: dict) -> Optional[Envelope]:
        return MessageEnvelope(envelope=envelope)


# register Envelope factory
Envelope.register(factory=EnvelopeFactory())
