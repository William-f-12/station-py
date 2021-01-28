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
    Messenger
    ~~~~~~~~~

    Transform and send message
"""

import weakref
from abc import abstractmethod
from typing import Optional, Union

from dimp import SymmetricKey, ID
from dimp import InstantMessage, SecureMessage, ReliableMessage
from dimp import ContentType, Content, FileContent
from dimp import EntityDelegate
from dimp import Transceiver

from .cpu import ContentProcessor, FileContentProcessor

from .delegate import Callback, CompletionHandler
from .delegate import MessengerDelegate, MessengerDataSource
from .facebook import Facebook


class Messenger(Transceiver):

    def __init__(self):
        super().__init__()
        self.__delegate: Optional[weakref.ReferenceType] = None
        self.__data_source: Optional[weakref.ReferenceType] = None

        self.__transmitter: Optional[weakref.ReferenceType] = None

        self.__facebook: Optional[Facebook] = None
        self.__message_packer = None
        self.__message_processor = None
        self.__message_transmitter = None

    #
    #   Delegate for sending data
    #
    @property
    def delegate(self) -> Optional[MessengerDelegate]:
        if self.__delegate is not None:
            return self.__delegate()

    @delegate.setter
    def delegate(self, value: Optional[MessengerDelegate]):
        self.__delegate = weakref.ref(value)

    #
    #   Delegate for saving message
    #
    @property
    def data_source(self) -> Optional[MessengerDataSource]:
        if self.__data_source is not None:
            return self.__data_source()

    @data_source.setter
    def data_source(self, value: Optional[MessengerDataSource]):
        self.__data_source = weakref.ref(value)

    #
    #   Delegate for getting entity
    #
    @property
    def barrack(self) -> EntityDelegate:
        delegate = super().barrack
        if delegate is None:
            delegate = self.facebook
        return delegate

    @barrack.setter
    def barrack(self, delegate: EntityDelegate):
        Transceiver.barrack.__set__(self, delegate)
        if isinstance(delegate, Facebook):
            self.__facebook = delegate

    @property
    def facebook(self) -> Facebook:
        if self.__facebook is None:
            self.__facebook = self._create_facebook()
        return self.__facebook

    @abstractmethod
    def _create_facebook(self) -> Facebook:
        raise NotImplemented

    #
    #   Message Packer
    #
    @property
    def packer(self) -> Transceiver.Packer:
        delegate = super().packer
        if delegate is None:
            delegate = self.__get_packer()
        return delegate

    @packer.setter
    def packer(self, delegate: Transceiver.Packer):
        Transceiver.packer.__set__(self, delegate)
        from .packer import MessagePacker
        if isinstance(delegate, MessagePacker):
            self.__message_packer = delegate

    def __get_packer(self):  # -> MessagePacker:
        if self.__message_packer is None:
            self.__message_packer = self._create_packer()
        return self.__message_packer

    def _create_packer(self):  # -> MessagePacker:
        from .packer import MessagePacker
        return MessagePacker(messenger=self)

    #
    #   Message Processor
    #
    @property
    def processor(self) -> Transceiver.Processor:
        delegate = super().processor
        if delegate is None:
            delegate = self.__get_processor()
        return delegate

    @processor.setter
    def processor(self, delegate: Transceiver.Processor):
        Transceiver.processor.__set__(self, delegate)
        from .processor import MessageProcessor
        if isinstance(delegate, MessageProcessor):
            self.__message_processor = delegate

    def __get_processor(self):  # -> MessageProcessor
        if self.__message_processor is None:
            self.__message_processor = self._create_processor()
        return self.__message_processor

    def _create_processor(self):  # -> MessageProcessor
        from .processor import MessageProcessor
        return MessageProcessor(messenger=self)

    #
    #   Message Transmitter
    #
    class Transmitter:

        @abstractmethod
        def send_content(self, sender: ID, receiver: ID, content: Content,
                         callback: Optional[Callback] = None, priority: int = 0) -> bool:
            """
            Send message content to receiver

            :param sender:   sender ID
            :param receiver: receiver ID
            :param content:  message content
            :param callback: if needs callback, set it here
            :param priority: task priority (smaller is faster)
            :return: True on success
            """
            raise NotImplemented

        @abstractmethod
        def send_message(self, msg: Union[InstantMessage, ReliableMessage],
                         callback: Optional[Callback] = None, priority: int = 0) -> bool:
            """
            Send instant message (encrypt and sign) onto DIM network

            :param msg:      instant message
            :param callback: callback function
            :param priority: task priority
            :return:         False on data/delegate error
            """
            raise NotImplemented

    @property
    def transmitter(self) -> Transmitter:
        if self.__transmitter is None:
            delegate = None
        else:
            delegate = self.__transmitter()
        if delegate is None:
            delegate = self.__get_transmitter()
        return delegate

    @transmitter.setter
    def transmitter(self, delegate: Transmitter):
        self.__transmitter = weakref.ref(delegate)
        from .transmitter import MessageTransmitter
        if isinstance(delegate, MessageTransmitter):
            self.__message_transmitter = delegate

    def __get_transmitter(self):  # -> MessageTransmitter:
        if self.__message_transmitter is None:
            self.__message_transmitter = self._create_transmitter()
        return self.__message_transmitter

    def _create_transmitter(self):  # -> MessageTransmitter:
        from .transmitter import MessageTransmitter
        return MessageTransmitter(messenger=self)

    #
    #   FPU
    #
    def __file_content_processor(self) -> FileContentProcessor:
        cpu = ContentProcessor.processor_for_type(ContentType.FILE)
        assert isinstance(cpu, FileContentProcessor), 'failed to get file content processor'
        cpu.messenger = self
        return cpu

    #
    #   InstantMessageDelegate
    #
    def serialize_content(self, content: Content, key: SymmetricKey, msg: InstantMessage) -> bytes:
        # check attachment for File/Image/Audio/Video message content before
        if isinstance(content, FileContent):
            fpu = self.__file_content_processor()
            fpu.upload(content=content, password=key, msg=msg)
        return super().serialize_content(content=content, key=key, msg=msg)

    def encrypt_key(self, data: bytes, receiver: ID, msg: InstantMessage) -> Optional[bytes]:
        facebook = self.facebook
        pk = facebook.public_key_for_encryption(identifier=receiver)
        if pk is None:
            # save this message in a queue waiting receiver's meta response
            self.suspend_message(msg=msg)
            # raise LookupError('failed to get encrypt key for receiver: %s' % receiver)
            return None
        return super().encrypt_key(data=data, receiver=receiver, msg=msg)

    #
    #   SecureMessageDelegate
    #
    def deserialize_content(self, data: bytes, key: SymmetricKey, msg: SecureMessage) -> Optional[Content]:
        content = super().deserialize_content(data=data, key=key, msg=msg)
        if content is None:
            raise AssertionError('failed to deserialize message content: %s' % msg)
        # check attachment for File/Image/Audio/Video message content after
        if isinstance(content, FileContent):
            fpu = self.__file_content_processor()
            fpu.download(content=content, password=key, msg=msg)
        return content

    #
    #   Interfaces for transmitting message
    #
    def send_content(self, sender: Optional[ID], receiver: ID, content: Content,
                     callback: Optional[Callback] = None, priority: int = 0) -> bool:
        if sender is None:
            # Application Layer should make sure user is already login before it send message to server.
            # Application layer should put message into queue so that it will send automatically after user login
            user = self.facebook.current_user
            assert user is not None, 'failed to get current user'
            sender = user.identifier

        return self.transmitter.send_content(sender=sender, receiver=receiver, content=content,
                                             callback=callback, priority=priority)

    def send_message(self, msg: Union[InstantMessage, ReliableMessage],
                     callback: Optional[Callback] = None, priority: int = 0) -> bool:
        return self.transmitter.send_message(msg=msg, callback=callback, priority=priority)

    #
    #   Interfaces for Station
    #
    def upload_data(self, data: bytes, msg: InstantMessage) -> str:
        return self.delegate.upload_data(data=data, msg=msg)

    def download_data(self, url: str, msg: InstantMessage) -> Optional[bytes]:
        return self.delegate.download_data(url=url, msg=msg)

    def send_package(self, data: bytes, handler: CompletionHandler, priority: int = 0) -> bool:
        return self.delegate.send_package(data=data, handler=handler, priority=priority)

    #
    #   Interfaces for Message Storage
    #

    def save_message(self, msg: InstantMessage) -> bool:
        return self.data_source.save_message(msg=msg)

    def suspend_message(self, msg: Union[ReliableMessage, InstantMessage]) -> bool:
        return self.data_source.suspend_message(msg=msg)


class MessageCallback(CompletionHandler):

    def __init__(self, msg: ReliableMessage, cb: Callback):
        super().__init__()
        self.msg = msg
        self.callback = cb

    def success(self):
        if self.callback is not None:
            self.callback.finished(result=self.msg, error=None)

    def failed(self, error):
        if self.callback is not None:
            self.callback.finished(result=self.msg, error=error)
