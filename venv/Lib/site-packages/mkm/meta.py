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
from typing import Optional, Union

from .crypto import base64_encode, base64_decode, utf8_encode
from .crypto import Map, Dictionary
from .crypto import VerifyKey, SignKey, PublicKey

from .types import NetworkType, MetaType, meta_has_seed
from .address import Address
from .identifier import ID


class Meta(Map):
    """This class is used to generate entity ID

        User/Group Meta data
        ~~~~~~~~~~~~~~~~~~~~

        data format: {
            version: 1,          // meta version
            seed: "moKy",        // user/group name
            key: "{public key}", // PK = secp256k1(SK);
            fingerprint: "..."   // CT = sign(seed, SK);
        }

        algorithm:
            fingerprint = sign(seed, SK);
    """

    @property
    @abstractmethod
    def type(self) -> int:
        """
        Meta algorithm version

            0x01 - username@address
            0x02 - btc_address
            0x03 - username@btc_address
            0x04 - eth_address
            0x05 - username@eth_address
            ...
        """
        raise NotImplemented

    @property
    @abstractmethod
    def key(self) -> VerifyKey:
        """
        Public key (used for signature)

            RSA
            ECC

        :return: public key
        """
        raise NotImplemented

    @property
    @abstractmethod
    def seed(self) -> Optional[str]:
        """
        Seed to generate fingerprint

        :return: ID.name
        """
        raise NotImplemented

    @property
    @abstractmethod
    def fingerprint(self) -> Optional[bytes]:
        """
        Fingerprint to verify ID and public key

            Build: fingerprint = sign(seed, privateKey)
            Check: verify(seed, fingerprint, publicKey)

        :return: signature
        """
        raise NotImplemented

    @property
    @abstractmethod
    def valid(self) -> bool:
        """
        Check meta valid
        (must call this when received a new meta from network)

        :return: True on valid
        """
        raise NotImplemented

    @abstractmethod
    def generate_identifier(self, network: Union[NetworkType, int], terminal: Optional[str]=None) -> Optional[ID]:
        """
        Generate ID with terminal

        :param network:  ID.type
        :param terminal: ID.terminal
        :return: ID
        """
        raise NotImplemented

    @abstractmethod
    def match_identifier(self, identifier: ID) -> bool:
        """
        Check whether meta match with entity ID
        (must call this when received a new meta from network)

        :param identifier: entity ID
        :return: True on matched
        """
        raise NotImplemented

    @abstractmethod
    def match_key(self, key: VerifyKey) -> bool:
        """
        Check whether meta match with public key

        :param key: public key
        :return: True on matched
        """
        raise NotImplemented

    #
    #   Meta factory
    #
    class Factory:

        @abstractmethod
        def create_meta(self, key: VerifyKey, seed: Optional[str] = None,
                        fingerprint: Union[bytes, str, None] = None):  # -> Meta:
            """
            Create meta

            :param key:         public key
            :param seed:        ID.name
            :param fingerprint: sKey.sign(seed)
            :return: Meta
            """
            raise NotImplemented

        @abstractmethod
        def generate_meta(self, key: SignKey, seed: Optional[str] = None):  # -> Meta:
            """
            Generate meta

            :param key:  private key
            :param seed: ID.name
            :return: Meta
            """
            raise NotImplemented

        @abstractmethod
        def parse_meta(self, meta: dict):  # -> Optional[Meta]:
            """
            Parse map object to meta

            :param meta: meta info
            :return: Meta
            """
            raise NotImplemented

    __factories = {}

    @classmethod
    def register(cls, version: Union[MetaType, int], factory: Factory):
        if isinstance(version, MetaType):
            version = version.value
        cls.__factories[version] = factory

    @classmethod
    def factory(cls, version: Union[MetaType, int]) -> Optional[Factory]:
        if isinstance(version, MetaType):
            version = version.value
        return cls.__factories.get(version)

    @classmethod
    def create(cls, version: Union[MetaType, int], key: VerifyKey,
               seed: Optional[str]=None, fingerprint: Union[bytes, str, None]=None):  # -> Optional[Meta]:
        factory = cls.factory(version=version)
        assert factory is not None, 'meta type not support: %d' % version
        return factory.create_meta(key=key, seed=seed, fingerprint=fingerprint)

    @classmethod
    def generate(cls, version: Union[MetaType, int], key: SignKey, seed: Optional[str]=None):  # -> Optional[Meta]:
        factory = cls.factory(version=version)
        assert factory is not None, 'meta type not support: %d' % version
        return factory.generate_meta(key=key, seed=seed)

    @classmethod
    def parse(cls, meta: dict):  # -> Optional[Meta]:
        if meta is None:
            return None
        elif isinstance(meta, cls):
            return meta
        elif isinstance(meta, Map):
            meta = meta.dictionary
        version = meta_type(meta=meta)
        factory = cls.factory(version=version)
        if factory is None:
            factory = cls.factory(version=0)  # unknown
            assert factory is not None, 'cannot parse meta: %s' % meta
        return factory.parse_meta(meta=meta)


"""
    Implements
    ~~~~~~~~~~
"""


def meta_type(meta: dict) -> int:
    version = meta.get('type')
    if version is None:
        version = meta.get('version')
    return int(version)


def meta_key(meta: dict) -> VerifyKey:
    key = meta.get('key')
    return PublicKey.parse(key=key)


def meta_seed(meta: dict) -> Optional[str]:
    return meta.get('seed')


def meta_fingerprint(meta: dict) -> Optional[bytes]:
    fingerprint = meta.get('fingerprint')
    if fingerprint is not None:
        return base64_decode(string=fingerprint)


class BaseMeta(Dictionary, Meta):

    def __init__(self, meta: Optional[dict]=None,
                 version: Union[MetaType, int]=0, key: Optional[VerifyKey]=None,
                 seed: Optional[str]=None, fingerprint: Union[bytes, str, None]=None):
        super().__init__(dictionary=meta)
        # pre-process
        if isinstance(version, MetaType):
            version = version.value
        if fingerprint is None:
            base64 = None
        elif isinstance(fingerprint, bytes):
            base64 = base64_encode(data=fingerprint)
        else:
            assert isinstance(fingerprint, str), 'meta.fingerprint error: %s' % fingerprint
            base64 = fingerprint
            fingerprint = base64_decode(string=base64)
        # set values
        self.__type = version
        self.__key = key
        self.__seed = seed
        self.__fingerprint = fingerprint
        self.__status = 0  # 1 for valid, -1 for invalid
        # set values to inner dictionary
        if version > 0:
            self['version'] = version
        if key is not None:
            self['key'] = key.dictionary
        if seed is not None:
            self['seed'] = seed
        if fingerprint is not None:
            self['fingerprint'] = base64

    @property
    def has_seed(self) -> bool:
        return meta_has_seed(version=self.type)

    @property
    def type(self) -> int:
        if self.__type is 0:
            self.__type = meta_type(meta=self.dictionary)
        return self.__type

    @property
    def key(self) -> VerifyKey:
        if self.__key is None:
            self.__key = meta_key(meta=self.dictionary)
        return self.__key

    @property
    def seed(self) -> Optional[str]:
        if self.__seed is None and self.has_seed:
            self.__seed = meta_seed(meta=self.dictionary)
        return self.__seed

    @property
    def fingerprint(self) -> Optional[bytes]:
        if self.__fingerprint is None and self.has_seed:
            self.__fingerprint = meta_fingerprint(meta=self.dictionary)
        return self.__fingerprint

    @property
    def valid(self) -> bool:
        if self.__status is 0:
            key = self.key
            if key is None:
                # meta.key should not be empty
                self.__status = -1
            elif self.has_seed:
                seed = self.seed
                fingerprint = self.fingerprint
                if seed is None or fingerprint is None:
                    # seed and fingerprint should not be empty
                    self.__status = -1
                elif key.verify(data=utf8_encode(string=seed), signature=fingerprint):
                    # fingerprint matched
                    self.__status = 1
                else:
                    # fingerprint not matched
                    self.__status = -1
            else:
                # BTC, ETH, ...
                self.__status = 1
        return self.__status == 1

    @abstractmethod
    def generate_address(self, network: Union[NetworkType, int]) -> Address:
        """
        Generate address

        :param network: ID.type
        :return: Address
        """
        raise NotImplemented

    def generate_identifier(self, network: Union[NetworkType, int], terminal: Optional[str]=None) -> Optional[ID]:
        address = self.generate_address(network=network)
        if address is not None:
            return ID.create(address=address, name=self.seed, terminal=terminal)

    def match_identifier(self, identifier: ID) -> bool:
        if self.valid and self.seed == identifier.name:
            return self.generate_address(network=identifier.type) == identifier.address

    def match_key(self, key: VerifyKey) -> bool:
        if not self.valid:
            return False
        if self.key == key:
            return True
        if self.has_seed:
            # check whether keys equal by verifying signature
            seed = self.seed
            fingerprint = self.fingerprint
            return key.verify(data=utf8_encode(string=seed), signature=fingerprint)
        else:
            # NOTICE: ID with BTC/ETH address has no username, so
            #         just compare the key.data to check matching
            return False
