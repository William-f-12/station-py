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

import copy
from abc import abstractmethod
from typing import Any, Optional, Union, Tuple, Iterator, Iterable
from typing import Mapping, MutableMapping, ItemsView, KeysView, ValuesView

from .string import String


class Wrapper:
    """
        Wrapper for dict, list, str
    """

    @classmethod
    def unwrap(cls, o: Any, circularly: bool = False) -> Any:
        # unwrap string
        if isinstance(o, String):
            return o.string
        if isinstance(o, str):
            return o
        # unwrap container
        if circularly:
            # unwrap map circularly
            if isinstance(o, Map):
                return Map.unwrap(o.dictionary, circularly=True)
            if isinstance(o, dict):
                return Map.unwrap(o, circularly=True)
            # unwrap list circularly
            if isinstance(o, Array):
                return Array.unwrap(o.array, circularly=True)
            if isinstance(o, list):
                return Array.unwrap(o, circularly=True)
        else:
            # unwrap map
            if isinstance(o, Map):
                return o.dictionary
            # unwrap list
            if isinstance(o, Array):
                return o.array
        # others
        return o


class Array:
    """
        List: Any
    """

    @classmethod
    def unwrap(cls, a: list, circularly: bool=False) -> list:
        # unwrap list container
        if isinstance(a, Array):
            a = a.array
        if not circularly:
            return a
        # unwrap items circularly
        t = []
        for o in a:
            item = Wrapper.unwrap(o, circularly=True)
            t.append(item)
        return t

    @property
    @abstractmethod
    def array(self) -> list:
        raise NotImplemented

    @property
    @abstractmethod
    def copy_array(self, deep_copy: bool=False) -> list:
        raise NotImplemented


class Map(MutableMapping):
    """
        Mapping: str -> Any
    """

    @classmethod
    def unwrap(cls, d: dict, circularly: bool = False) -> dict:
        # unwrap map container
        if isinstance(d, Map):
            d = d.dictionary
        if not circularly:
            return d
        # unwrap keys, values circularly
        t = {}
        for k in d:
            v = d[k]
            key = String.unwrap(k)
            value = Wrapper.unwrap(v, circularly=True)
            t[key] = value
        return t

    @property
    @abstractmethod
    def dictionary(self) -> dict:
        raise NotImplemented

    @abstractmethod
    def copy_dictionary(self, deep_copy: bool=False) -> dict:
        raise NotImplemented


class Dictionary(Map):
    """
        A container sharing the same inner dictionary
    """

    # def __new__(cls, dictionary: Optional[dict]=None):
    #     return super().__new__(cls, dictionary=dictionary)

    def __init__(self, dictionary: Optional[dict]=None):
        super().__init__()
        if dictionary is None:
            self.__dictionary = {}
        elif isinstance(dictionary, Dictionary):
            self.__dictionary = dictionary.dictionary
        else:
            assert isinstance(dictionary, dict), 'dictionary error: %s' % dictionary
            self.__dictionary = dictionary

    @property
    def dictionary(self) -> dict:
        return self.__dictionary

    def copy_dictionary(self, deep_copy: bool=False) -> dict:
        if deep_copy:
            copy.deepcopy(self.__dictionary)
        else:
            return self.__dictionary.copy()

    def clear(self):
        """ D.clear() -> None.  Remove all items from D. """
        self.__dictionary.clear()

    def copy(self):
        """ D.copy() -> a shallow copy of D """
        dictionary = self.__dictionary.copy()
        return Dictionary(dictionary=dictionary)

    @staticmethod
    def fromkeys(seq: Iterable[str], value: Optional[Any]=None):
        """ Create a new dictionary with keys from iterable and values set to value. """
        dictionary = dict.fromkeys(seq=seq, value=value)
        return Dictionary(dictionary=dictionary)

    def get(self, k: str, default: Optional[Any]=None) -> Optional[Any]:
        """ Return the value for key if key is in the dictionary, else default. """
        return self.__dictionary.get(k, default)

    def items(self) -> ItemsView[str, Any]:
        """ D.items() -> a set-like object providing a view on D's items """
        return self.__dictionary.items()

    def keys(self) -> KeysView[str]:
        """ D.keys() -> a set-like object providing a view on D's keys """
        return self.__dictionary.keys()

    def pop(self, k: str, default: Optional[Any]=None) -> Optional[Any]:
        """
        D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised
        """
        return self.__dictionary.pop(k, default)

    def popitem(self) -> Tuple[str, Any]:
        """
        D.popitem() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if D is empty.
        """
        return self.__dictionary.popitem()

    def setdefault(self, k: str, default: Optional[Any]=None) -> Any:
        """
        Insert key with a value of default if key is not in the dictionary.

        Return the value for key if key is in the dictionary, else default.
        """
        self.__dictionary.setdefault(k, default)

    def update(self, __m: Mapping[str, Any], **kwargs: Any):
        self.__dictionary.update(__m)

    def values(self) -> ValuesView[Any]:
        """ D.values() -> an object providing a view on D's values """
        return self.__dictionary.values()

    def __contains__(self, o) -> bool:
        """ True if the dictionary has the specified key, else False. """
        return self.__dictionary.__contains__(o)

    def __delitem__(self, v: str):
        """ Delete self[key]. """
        self.__dictionary.__delitem__(v)

    def __eq__(self, o: Union[dict, Map]) -> bool:
        """ Return self==value. """
        if isinstance(o, Map):
            if self is o:
                return True
            o = o.dictionary
        return self.__dictionary.__eq__(o)

    # def __getattribute__(self, name: str) -> Any:
    #     """ Return getattr(self, name). """
    #     if isinstance(name, String):
    #         name = name.string
    #     return self.__dictionary.__getattribute__(name=name)

    def __getitem__(self, k: str) -> Any:
        """ x.__getitem__(y) <==> x[y] """
        return self.__dictionary.__getitem__(k)

    def __ge__(self, other) -> bool:
        """ Return self>=value. """
        pass

    def __gt__(self, other) -> bool:
        """ Return self>value. """
        pass

    def __iter__(self) -> Iterator[str]:
        """ Implement iter(self). """
        return self.__dictionary.__iter__()

    def __len__(self) -> int:
        """ Return len(self). """
        return self.__dictionary.__len__()

    def __le__(self, other) -> bool:
        """ Return self<=value. """
        pass

    def __lt__(self, other) -> bool:
        """ Return self<value. """
        pass

    def __ne__(self, o: Union[dict, Map]) -> bool:
        """ Return self!=value. """
        if isinstance(o, Map):
            if self is o:
                return False
            o = o.dictionary
        return self.__dictionary.__ne__(o)

    def __repr__(self) -> str:
        """ Return repr(self). """
        return self.__dictionary.__repr__()

    def __setitem__(self, k: str, v: Optional[Any]):
        """ Set self[key] to value. """
        self.__dictionary.__setitem__(k, v)

    def __sizeof__(self) -> int:
        """ D.__sizeof__() -> size of D in memory, in bytes """
        return self.__dictionary.__sizeof__()

    __hash__ = None
