# -*- coding: utf-8 -*-
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

from typing import Optional, Union

from mkm.crypto.cryptography import key_algorithm
from mkm.meta import meta_type
from mkm.profile import document_identifier

from dimp import utf8_encode

from dimp import AsymmetricKey, SignKey, VerifyKey
from dimp import PublicKey
from dimp import PrivateKey
from dimp import SymmetricKey
from dimp import ID, Address, AddressFactory
from dimp import Meta, MetaType
from dimp import Document
from dimp import BaseDocument, BaseVisa, BaseBulletin

from .rsa import RSAPublicKey, RSAPrivateKey
from .ecc import ECCPublicKey, ECCPrivateKey
from .aes import AESKey
from .plain import PlainKey
from .btc import BTCAddress
from .eth import ETHAddress
from .meta import DefaultMeta, BTCMeta, ETHMeta


class GeneralPublicFactory(PublicKey.Factory):

    def parse_public_key(self, key: dict) -> Optional[PublicKey]:
        algorithm = key_algorithm(key=key)
        if algorithm == AsymmetricKey.RSA:
            return RSAPublicKey(key=key)
        if algorithm == AsymmetricKey.ECC:
            return ECCPublicKey(key=key)


class GeneralPrivateFactory(PrivateKey.Factory):

    def __init__(self, algorithm: str):
        super().__init__()
        self.__algorithm = algorithm

    def generate_private_key(self) -> Optional[PrivateKey]:
        if self.__algorithm == AsymmetricKey.RSA:
            return RSAPrivateKey()
        if self.__algorithm == AsymmetricKey.ECC:
            return ECCPrivateKey()

    def parse_private_key(self, key: dict) -> Optional[PrivateKey]:
        algorithm = key_algorithm(key=key)
        if algorithm == AsymmetricKey.RSA:
            return RSAPrivateKey(key=key)
        if algorithm == AsymmetricKey.ECC:
            return ECCPrivateKey(key=key)


class GeneralSymmetricFactory(SymmetricKey.Factory):

    def __init__(self, algorithm: str):
        super().__init__()
        self.__algorithm = algorithm
        self.__plain_key = PlainKey()

    def generate_symmetric_key(self) -> Optional[SymmetricKey]:
        if self.__algorithm == SymmetricKey.AES:
            return AESKey()
        if self.__algorithm == PlainKey.PLAIN:
            return self.__plain_key

    def parse_symmetric_key(self, key: dict) -> Optional[SymmetricKey]:
        algorithm = key_algorithm(key=key)
        if algorithm == SymmetricKey.AES:
            return AESKey(key=key)
        if algorithm == PlainKey.PLAIN:
            return self.__plain_key


class GeneralAddressFactory(AddressFactory):

    def create_address(self, address: str) -> Optional[Address]:
        if len(address) == 42:
            return ETHAddress.parse(address=address)
        return BTCAddress.parse(address=address)


class GeneralMetaFactory(Meta.Factory):

    def __init__(self, version: Union[MetaType, int]):
        super().__init__()
        self.__type = version

    def create_meta(self, key: VerifyKey, seed: Optional[str] = None, fingerprint: Optional[bytes] = None) -> Meta:
        if self.__type == MetaType.MKM:
            return DefaultMeta(version=self.__type, key=key, seed=seed, fingerprint=fingerprint)
        if self.__type in [MetaType.BTC, MetaType.ExBTC]:
            return BTCMeta(version=self.__type, key=key, seed=seed, fingerprint=fingerprint)
        if self.__type in [MetaType.ETH, MetaType.ExETH]:
            return ETHMeta(version=self.__type, key=key, seed=seed, fingerprint=fingerprint)

    def generate_meta(self, key: SignKey, seed: Optional[str] = None) -> Meta:
        if seed is None or len(seed) == 0:
            fingerprint = None
        else:
            fingerprint = key.sign(data=utf8_encode(string=seed))
        assert isinstance(key, PrivateKey), 'private key error: %s' % key
        return self.create_meta(key=key.public_key, seed=seed, fingerprint=fingerprint)

    def parse_meta(self, meta: dict) -> Optional[Meta]:
        version = meta_type(meta=meta)
        if version == MetaType.MKM:
            return DefaultMeta(meta=meta)
        if version in [MetaType.BTC, MetaType.ExBTC]:
            return BTCMeta(meta=meta)
        if version in [MetaType.ETH, MetaType.ExETH]:
            return ETHMeta(meta=meta)


class GeneralDocumentFactory(Document.Factory):

    def __init__(self, doc_type: str):
        super().__init__()
        self.__type = doc_type

    def get_type(self, identifier: ID) -> str:
        if self.__type == '*':
            if identifier.is_group:
                return Document.BULLETIN
            elif identifier.is_user:
                return Document.VISA
            else:
                return Document.PROFILE
        return self.__type

    def create_document(self, identifier: ID,
                        data: Union[bytes, str, None] = None, signature: Union[bytes, str, None] = None) -> Document:
        doc_type = self.get_type(identifier=identifier)
        if doc_type == Document.BULLETIN:
            return BaseBulletin(identifier=identifier, data=data, signature=signature)
        elif doc_type == Document.VISA:
            return BaseVisa(identifier=identifier, data=data, signature=signature)
        else:
            return BaseDocument(doc_type=doc_type, identifier=identifier, data=data, signature=signature)

    def parse_document(self, document: dict) -> Optional[Document]:
        identifier = document_identifier(document=document)
        if identifier is not None:
            doc_type = self.get_type(identifier=identifier)
            if doc_type == Document.BULLETIN:
                return BaseBulletin(document=document)
            elif doc_type == Document.VISA:
                return BaseVisa(document=document)
            else:
                return BaseDocument(document=document)


def register_key_factories():
    # Public Key: ECC
    factory = GeneralPublicFactory()
    PublicKey.register(algorithm=AsymmetricKey.ECC, factory=factory)
    # Public Key: RSA
    PublicKey.register(algorithm=AsymmetricKey.RSA, factory=factory)
    PublicKey.register(algorithm='SHA256withRSA', factory=factory)
    PublicKey.register(algorithm='RSA/ECB/PKCS1Padding', factory=factory)

    # Private Key: ECC
    factory = GeneralPrivateFactory(algorithm=AsymmetricKey.ECC)
    PrivateKey.register(algorithm=AsymmetricKey.ECC, factory=factory)

    # Private Key: RSA
    factory = GeneralPrivateFactory(algorithm=AsymmetricKey.RSA)
    PrivateKey.register(algorithm=AsymmetricKey.RSA, factory=factory)
    PrivateKey.register(algorithm='SHA256withRSA', factory=factory)
    PrivateKey.register(algorithm='RSA/ECB/PKCS1Padding', factory=factory)

    # Symmetric Key: AES
    factory = GeneralSymmetricFactory(algorithm=SymmetricKey.AES)
    SymmetricKey.register(algorithm=SymmetricKey.AES, factory=factory)
    SymmetricKey.register(algorithm='AES/CBC/PKCS7Padding', factory=factory)

    # Symmetric Key: Plain
    factory = GeneralSymmetricFactory(algorithm=PlainKey.PLAIN)
    SymmetricKey.register(algorithm=PlainKey.PLAIN, factory=factory)


def register_meta_factories():
    Meta.register(version=MetaType.MKM, factory=GeneralMetaFactory(version=MetaType.MKM))
    Meta.register(version=MetaType.BTC, factory=GeneralMetaFactory(version=MetaType.BTC))
    Meta.register(version=MetaType.ExBTC, factory=GeneralMetaFactory(version=MetaType.ExBTC))
    Meta.register(version=MetaType.ETH, factory=GeneralMetaFactory(version=MetaType.ETH))
    Meta.register(version=MetaType.ExETH, factory=GeneralMetaFactory(version=MetaType.ExETH))


def register_document_factories():
    Document.register(doc_type='*', factory=GeneralDocumentFactory(doc_type='*'))
    Document.register(doc_type=Document.VISA, factory=GeneralDocumentFactory(doc_type=Document.VISA))
    Document.register(doc_type=Document.PROFILE, factory=GeneralDocumentFactory(doc_type=Document.PROFILE))
    Document.register(doc_type=Document.BULLETIN, factory=GeneralDocumentFactory(doc_type=Document.BULLETIN))


#
#   Register all factories
#
register_key_factories()

Address.register(factory=GeneralAddressFactory())

register_meta_factories()

register_document_factories()
