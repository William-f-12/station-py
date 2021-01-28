# -*- coding: utf-8 -*-
#
#   Ming-Ke-Ming : Decentralized User Identity Authentication
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

from abc import abstractmethod
from typing import Optional, Union, Any

from .crypto import Map
from .crypto import VerifyKey, SignKey

from .identifier import ID


class TAI:
    """
        The Additional Information
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        'Meta' is the information for entity which never changed,
            which contains the key for verify signature;
        'TAI' is the variable part,
            which could contain a public key for asymmetric encryption.
    """

    @property
    @abstractmethod
    def valid(self) -> bool:
        """
        Check if signature matched

        :return: True on matched
        """
        raise NotImplemented

    #
    #  signature
    #

    @abstractmethod
    def verify(self, public_key: VerifyKey) -> bool:
        """
        Verify 'data' and 'signature' with public key

        :param public_key: public key in meta.key
        :return: True on signature matched
        """
        raise NotImplemented

    @abstractmethod
    def sign(self, private_key: SignKey) -> bytes:
        """
        Encode properties to 'data' and sign it to 'signature'

        :param private_key: private key match meta.key
        :return: signature
        """
        raise NotImplemented

    #
    #  properties
    #

    @property
    @abstractmethod
    def properties(self) -> Optional[dict]:
        """
        Get all properties when valid

        :return: inner dictionary
        """
        raise NotImplemented

    @abstractmethod
    def get_property(self, key: str) -> Optional[Any]:
        """
        Get property value with key

        :param key: property key
        :return: property value
        """
        raise NotImplemented

    @abstractmethod
    def set_property(self, key: str, value: Any=None):
        """
        Update property with key and data
        (this will clear 'data' and 'signature')

        :param key:   property key
        :param value: property value
        """
        raise NotImplemented


class Document(TAI, Map):

    #
    #  Document types
    #
    VISA = 'visa'          # for login/communication
    PROFILE = 'profile'    # for user info
    BULLETIN = 'bulletin'  # for group info

    @property
    @abstractmethod
    def type(self) -> str:
        """
        Get document type

        :return: doc type
        """
        raise NotImplemented

    @property
    @abstractmethod
    def identifier(self) -> ID:
        """
        Get entity ID

        :return: Entity ID
        """
        raise NotImplemented

    #
    #  properties getter/setter
    #
    @property
    def name(self) -> str:
        """
        Get entity name

        :return: name string
        """
        raise NotImplemented

    @name.setter
    def name(self, string: str):
        """
        Set entity name

        :param string: name string
        :return:
        """
        raise NotImplemented

    #
    #   Document factory
    #
    class Factory:

        @abstractmethod
        def create_document(self, identifier: ID,
                            data: Union[bytes, str, None]=None,
                            signature: Union[bytes, str, None]=None):  # -> Document:
            """
            1. Create a new empty document with entity ID

            2. Create document with data & signature loaded from local storage

            :param identifier: entity ID
            :param data:       document data
            :param signature:  document signature
            :return: Document
            """
            raise NotImplemented

        @abstractmethod
        def parse_document(self, document: dict):  # -> Optional[Document]:
            """
            Parse map object to entity document

            :param document:
            :return:
            """
            raise NotImplemented

    __factories = {}

    @classmethod
    def register(cls, doc_type: str, factory: Factory):
        cls.__factories[doc_type] = factory

    @classmethod
    def factory(cls, doc_type: str) -> Optional[Factory]:
        return cls.__factories.get(doc_type)

    @classmethod
    def create(cls, doc_type: str, identifier: ID, data: Union[bytes, str]=None, signature: Union[bytes, str]=None):
        factory = cls.factory(doc_type=doc_type)
        assert factory is not None, 'doc_type not support: %s' % doc_type
        return factory.create_document(identifier=identifier, data=data, signature=signature)

    @classmethod
    def parse(cls, document: dict):
        if document is None:
            return None
        elif isinstance(document, cls):
            return document
        elif isinstance(document, Map):
            document = document.dictionary
        doc_type = document_type(document=document)
        factory = cls.factory(doc_type=doc_type)
        if factory is None:
            factory = cls.factory(doc_type='*')  # unknown
            assert factory is not None, 'cannot parse document: %s' % document
        return factory.parse_document(document=document)


def document_type(document: dict) -> str:
    return document.get('type')
