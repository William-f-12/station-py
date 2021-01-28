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
    Delegates
    ~~~~~~~~~

    Delegates for Messenger
"""

from abc import abstractmethod
from typing import Optional, Union

from dimp import InstantMessage, ReliableMessage


class Callback:

    @abstractmethod
    def finished(self, result, error=None):
        raise NotImplemented


class CompletionHandler:

    @abstractmethod
    def success(self):
        raise NotImplemented

    @abstractmethod
    def failed(self, error):
        raise NotImplemented


class MessengerDelegate:

    @abstractmethod
    def upload_data(self, data: bytes, msg: InstantMessage) -> str:
        """
        Upload encrypted data to CDN

        :param data: encrypted file data
        :param msg:  instant message
        :return: download URL
        """
        raise NotImplemented

    @abstractmethod
    def download_data(self, url: str, msg: InstantMessage) -> Optional[bytes]:
        """
        Download encrypted data from CDN

        :param url: download URL
        :param msg: instant message
        :return: encrypted file data
        """
        raise NotImplemented

    @abstractmethod
    def send_package(self, data: bytes, handler: CompletionHandler, priority: int = 0) -> bool:
        """
        Send out a data package onto network

        :param data:     package data
        :param handler:  completion handler
        :param priority: task priority (smaller is faster)
        :return: True on success
        """
        raise NotImplemented


class MessengerDataSource:

    @abstractmethod
    def save_message(self, msg: InstantMessage) -> bool:
        """
        Save the message into local storage

        :param msg: instant message
        :return: True on success
        """
        raise NotImplemented

    # NOTICE: this function is for Client
    #         if the client cannot get verify/encrypt message for contact,
    #         it means you should suspend it and query meta from DIM station first
    @abstractmethod
    def suspend_message(self, msg: Union[InstantMessage, ReliableMessage]) -> bool:
        """
        1. Suspend the sending message for the receiver's meta & visa,
           or group meta when received new message
        2. Suspend the received message for the sender's meta

        :param msg: instant/reliable message
        :return:
        """
        raise NotImplemented
