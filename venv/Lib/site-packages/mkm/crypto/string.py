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

from typing import Optional, Union, Any, Tuple, Mapping, List, Iterable, Iterator


class String:
    """
        A container with inner string
    """

    @classmethod
    def unwrap(cls, s: str) -> str:
        # unwrap string container
        if isinstance(s, String):
            return s.string
        # assert isinstance(s, str)
        return s

    # def __new__(cls, string: Optional[str]=None):
    #     return super().__new__(cls, string=string)

    def __init__(self, string: Optional[str]=None):
        super().__init__()
        if string is None:
            self.__string = ''
        elif isinstance(string, String):
            self.__string = string.string
        else:
            assert isinstance(string, str), 'string error: %s' % string
            self.__string = string

    @property
    def string(self) -> str:
        return self.__string

    def capitalize(self):
        """
        Return a capitalized version of the string.

        More specifically, make the first character have upper case and the rest lower
        case.
        """
        string = self.__string.capitalize()
        return String(string=string)

    def casefold(self):
        """ Return a version of the string suitable for caseless comparisons. """
        string = self.__string.casefold()
        return String(string=string)

    def center(self, width: int, fillchar: str=' '):
        """
        Return a centered string of length width.

        Padding is done using the specified fill character (default is a space).
        """
        if isinstance(fillchar, String):
            fillchar = fillchar.string
        string = self.__string.center(width, fillchar)
        return String(string=string)

    def count(self, x: str, __start: Optional[int]=None, __end: Optional[int]=None) -> int:
        """
        S.count(sub[, start[, end]]) -> int

        Return the number of non-overlapping occurrences of substring sub in
        string S[start:end].  Optional arguments start and end are
        interpreted as in slice notation.
        """
        if isinstance(x, String):
            x = x.string
        return self.__string.count(x, __start, __end)

    def encode(self, encoding: str='utf-8', errors: str='strict') -> bytes:
        """
        Encode the string using the codec registered for encoding.

          encoding
            The encoding in which to encode the string.
          errors
            The error handling scheme to use for encoding errors.
            The default is 'strict' meaning that encoding errors raise a
            UnicodeEncodeError.  Other possible values are 'ignore', 'replace' and
            'xmlcharrefreplace' as well as any other name registered with
            codecs.register_error that can handle UnicodeEncodeErrors.
        """
        return self.__string.encode(encoding, errors)

    def endswith(self, suffix: str, start: Optional[int]=None, end: Optional[int]=None) -> bool:
        """
        S.endswith(suffix[, start[, end]]) -> bool

        Return True if S ends with the specified suffix, False otherwise.
        With optional start, test S beginning at that position.
        With optional end, stop comparing S at that position.
        suffix can also be a tuple of strings to try.
        """
        if isinstance(suffix, String):
            suffix = suffix.string
        return self.__string.endswith(suffix, start, end)

    def expandtabs(self, tabsize: int=8):
        """
        Return a copy where all tab characters are expanded using spaces.

        If tabsize is not given, a tab size of 8 characters is assumed.
        """
        string = self.__string.expandtabs(tabsize)
        return String(string=string)

    def find(self, sub: str, __start: Optional[int]=None, __end: Optional[int]=None) -> int:
        """
        S.find(sub[, start[, end]]) -> int

        Return the lowest index in S where substring sub is found,
        such that sub is contained within S[start:end].  Optional
        arguments start and end are interpreted as in slice notation.

        Return -1 on failure.
        """
        if isinstance(sub, String):
            sub = sub.string
        return self.__string.find(sub, __start, __end)

    def format(self, *args, **kwargs):
        """
        S.format(*args, **kwargs) -> str

        Return a formatted version of S, using substitutions from args and kwargs.
        The substitutions are identified by braces ('{' and '}').
        """
        string = self.__string.format(args, kwargs)
        return String(string=string)

    def format_map(self, mapping: Mapping[str, Any]):
        """
        S.format_map(mapping) -> str

        Return a formatted version of S, using substitutions from mapping.
        The substitutions are identified by braces ('{' and '}').
        """
        from .dictionary import Map
        if isinstance(mapping, Map):
            mapping = mapping.dictionary
        string = self.__string.format_map(map=mapping)
        return String(string=string)

    def index(self, sub: str, __start: Optional[int]=None, __end: Optional[int]=None) -> int:
        """
        S.index(sub[, start[, end]]) -> int

        Return the lowest index in S where substring sub is found,
        such that sub is contained within S[start:end].  Optional
        arguments start and end are interpreted as in slice notation.

        Raises ValueError when the substring is not found.
        """
        if isinstance(sub, String):
            sub = sub.string
        return self.__string.index(sub, __start, __end)

    def isalnum(self) -> bool:
        """
        Return True if the string is an alpha-numeric string, False otherwise.

        A string is alpha-numeric if all characters in the string are alpha-numeric and
        there is at least one character in the string.
        """
        return self.__string.isalnum()

    def isalpha(self) -> bool:
        """
        Return True if the string is an alphabetic string, False otherwise.

        A string is alphabetic if all characters in the string are alphabetic and there
        is at least one character in the string.
        """
        return self.__string.isalpha()

    def isascii(self) -> bool:
        """
        Return True if all characters in the string are ASCII, False otherwise.

        ASCII characters have code points in the range U+0000-U+007F.
        Empty string is ASCII too.
        """
        pass

    def isdecimal(self) -> bool:
        """
        Return True if the string is a decimal string, False otherwise.

        A string is a decimal string if all characters in the string are decimal and
        there is at least one character in the string.
        """
        return self.__string.isdecimal()

    def isdigit(self) -> bool:
        """
        Return True if the string is a digit string, False otherwise.

        A string is a digit string if all characters in the string are digits and there
        is at least one character in the string.
        """
        return self.__string.isdigit()

    def isidentifier(self) -> bool:
        """
        Return True if the string is a valid Python identifier, False otherwise.

        Use keyword.iskeyword() to test for reserved identifiers such as "def" and
        "class".
        """
        return self.__string.isidentifier()

    def islower(self) -> bool:
        """
        Return True if the string is a lowercase string, False otherwise.

        A string is lowercase if all cased characters in the string are lowercase and
        there is at least one cased character in the string.
        """
        return self.__string.islower()

    def isnumeric(self) -> bool:
        """
        Return True if the string is a numeric string, False otherwise.

        A string is numeric if all characters in the string are numeric and there is at
        least one character in the string.
        """
        return self.__string.isnumeric()

    def isprintable(self) -> bool:
        """
        Return True if the string is printable, False otherwise.

        A string is printable if all of its characters are considered printable in
        repr() or if it is empty.
        """
        return self.__string.isprintable()

    def isspace(self) -> bool:
        """
        Return True if the string is a whitespace string, False otherwise.

        A string is whitespace if all characters in the string are whitespace and there
        is at least one character in the string.
        """
        return self.__string.isspace()

    def istitle(self) -> bool:
        """
        Return True if the string is a title-cased string, False otherwise.

        In a title-cased string, upper- and title-case characters may only
        follow uncased characters and lowercase characters only cased ones.
        """
        return self.__string.istitle()

    def isupper(self) -> bool:
        """
        Return True if the string is an uppercase string, False otherwise.

        A string is uppercase if all cased characters in the string are uppercase and
        there is at least one cased character in the string.
        """
        return self.__string.isupper()

    def join(self, iterable: Iterable[str]):
        """
        Concatenate any number of strings.

        The string whose method is called is inserted in between each given string.
        The result is returned as a new string.

        Example: '.'.join(['ab', 'pq', 'rs']) -> 'ab.pq.rs'
        """
        string = self.__string.join(iterable)
        return String(string=string)

    def ljust(self, width: int, fillchar: str=' '):
        """
        Return a left-justified string of length width.

        Padding is done using the specified fill character (default is a space).
        """
        if isinstance(fillchar, String):
            fillchar = fillchar.string
        string = self.__string.ljust(width, fillchar)
        return String(string=string)

    def lower(self):
        """ Return a copy of the string converted to lowercase. """
        string = self.__string.lower()
        return String(string=string)

    def lstrip(self, chars: Optional[str]=None):
        """
        Return a copy of the string with leading whitespace removed.

        If chars is given and not None, remove characters in chars instead.
        """
        if isinstance(chars, String):
            chars = chars.string
        string = self.__string.lstrip(chars)
        return String(string=string)

    def maketrans(self, *args, **kwargs):
        """
        Return a translation table usable for str.translate().

        If there is only one argument, it must be a dictionary mapping Unicode
        ordinals (integers) or characters to Unicode ordinals, strings or None.
        Character keys will be then converted to ordinals.
        If there are two arguments, they must be strings of equal length, and
        in the resulting dictionary, each character in x will be mapped to the
        character at the same position in y. If there is a third argument, it
        must be a string, whose characters will be mapped to None in the result.
        """
        pass

    def partition(self, sep: str) -> Tuple[str, str, str]:
        """
        Partition the string into three parts using the given separator.

        This will search for the separator in the string.  If the separator is found,
        returns a 3-tuple containing the part before the separator, the separator
        itself, and the part after it.

        If the separator is not found, returns a 3-tuple containing the original string
        and two empty strings.
        """
        if isinstance(sep, String):
            sep = sep.string
        return self.__string.partition(sep)

    def replace(self, old: str, new: str, count: int=-1):
        """
        Return a copy with all occurrences of substring old replaced by new.

          count
            Maximum number of occurrences to replace.
            -1 (the default value) means replace all occurrences.

        If the optional argument count is given, only the first count occurrences are
        replaced.
        """
        if isinstance(old, String):
            old = old.string
        if isinstance(new, String):
            new = new.string
        string = self.__string.replace(old, new, count)
        return String(string=string)

    def rfind(self, sub: str, __start: Optional[int]=None, __end: Optional[int]=None) -> int:
        """
        S.rfind(sub[, start[, end]]) -> int

        Return the highest index in S where substring sub is found,
        such that sub is contained within S[start:end].  Optional
        arguments start and end are interpreted as in slice notation.

        Return -1 on failure.
        """
        if isinstance(sub, String):
            sub = sub.string
        return self.__string.rfind(sub, __start, __end)

    def rindex(self, sub: str, __start: Optional[int]=None, __end: Optional[int]=None) -> int:
        """
        S.rindex(sub[, start[, end]]) -> int

        Return the highest index in S where substring sub is found,
        such that sub is contained within S[start:end].  Optional
        arguments start and end are interpreted as in slice notation.

        Raises ValueError when the substring is not found.
        """
        if isinstance(sub, String):
            sub = sub.string
        return self.__string.rindex(sub, __start, __end)

    def rjust(self, width: int, fillchar: str=' '):
        """
        Return a right-justified string of length width.

        Padding is done using the specified fill character (default is a space).
        """
        if isinstance(fillchar, String):
            fillchar = fillchar.string
        string = self.__string.rjust(width, fillchar)
        return String(string=string)

    def rpartition(self, sep: str) -> Tuple[str, str, str]:
        """
        Partition the string into three parts using the given separator.

        This will search for the separator in the string, starting at the end. If
        the separator is found, returns a 3-tuple containing the part before the
        separator, the separator itself, and the part after it.

        If the separator is not found, returns a 3-tuple containing two empty strings
        and the original string.
        """
        if isinstance(sep, String):
            sep = sep.string
        return self.__string.rpartition(sep)

    def rsplit(self, sep: Optional[str]=None, maxsplit: int=-1) -> List[str]:
        """
        Return a list of the words in the string, using sep as the delimiter string.

          sep
            The delimiter according which to split the string.
            None (the default value) means split according to any whitespace,
            and discard empty strings from the result.
          maxsplit
            Maximum number of splits to do.
            -1 (the default value) means no limit.

        Splits are done starting at the end of the string and working to the front.
        """
        if isinstance(sep, String):
            sep = sep.string
        return self.__string.rsplit(sep, maxsplit)

    def rstrip(self, chars: Optional[str]=None):
        """
        Return a copy of the string with trailing whitespace removed.

        If chars is given and not None, remove characters in chars instead.
        """
        if isinstance(chars, String):
            chars = chars.string
        string = self.__string.rstrip(chars)
        return String(string=string)

    def split(self, sep: Optional[str]=None, maxsplit: int=-1) -> List[str]:
        """
        Return a list of the words in the string, using sep as the delimiter string.

          sep
            The delimiter according which to split the string.
            None (the default value) means split according to any whitespace,
            and discard empty strings from the result.
          maxsplit
            Maximum number of splits to do.
            -1 (the default value) means no limit.
        """
        if isinstance(sep, String):
            sep = sep.string
        return self.__string.split(sep, maxsplit)

    def splitlines(self, keepends: bool=False) -> List[str]:
        """
        Return a list of the lines in the string, breaking at line boundaries.

        Line breaks are not included in the resulting list unless keepends is given and
        true.
        """
        return self.__string.splitlines(keepends)

    def startswith(self, prefix, start: Optional[int]=None, end: Optional[int]=None) -> bool:
        """
        S.startswith(prefix[, start[, end]]) -> bool

        Return True if S starts with the specified prefix, False otherwise.
        With optional start, test S beginning at that position.
        With optional end, stop comparing S at that position.
        prefix can also be a tuple of strings to try.
        """
        if isinstance(prefix, String):
            prefix = prefix.string
        return self.__string.startswith(prefix, start, end)

    def strip(self, chars: Optional[str]=None):
        """
        Return a copy of the string with leading and trailing whitespace remove.

        If chars is given and not None, remove characters in chars instead.
        """
        if isinstance(chars, String):
            chars = chars.string
        string = self.__string.strip(chars)
        return String(string=string)

    def swapcase(self):
        """ Convert uppercase characters to lowercase and lowercase characters to uppercase. """
        string = self.__string.swapcase()
        return String(string=string)

    def title(self):
        """
        Return a version of the string where each word is titlecased.

        More specifically, words start with uppercased characters and all remaining
        cased characters have lower case.
        """
        string = self.__string.title()
        return String(string=string)

    def translate(self):
        """
        Replace each character in the string using the given translation table.

          table
            Translation table, which must be a mapping of Unicode ordinals to
            Unicode ordinals, strings, or None.

        The table must implement lookup/indexing via __getitem__, for instance a
        dictionary or list.  If this operation raises LookupError, the character is
        left untouched.  Characters mapped to None are deleted.
        """
        pass

    def upper(self):
        """ Return a copy of the string converted to uppercase. """
        string = self.__string.upper()
        return String(string=string)

    def zfill(self, width: int):
        """
        Pad a numeric string with zeros on the left, to fill a field of the given width.

        The string is never truncated.
        """
        string = self.__string.zfill(width)
        return String(string=string)

    def __add__(self, s: str):
        """ Return self+value. """
        if isinstance(s, String):
            s = s.string
        string = self.__string.__add__(s)
        return String(string=string)

    def __contains__(self, s: str) -> bool:
        """ Return key in self. """
        if isinstance(s, String):
            s = s.string
        return self.__string.__contains__(s)

    def __eq__(self, x: str) -> bool:
        """ Return self==value. """
        if isinstance(x, String):
            if self is x:
                return True
            x = x.string
        return self.__string.__eq__(x)

    def __format__(self, format_spec: str):
        """ Return a formatted version of the string as described by format_spec. """
        if isinstance(format_spec, String):
            format_spec = format_spec.string
        string = self.__string.__format__(format_spec)
        return String(string=string)

    # def __getattribute__(self, name: str) -> Any:
    #     """ Return getattr(self, name). """
    #     if isinstance(name, String):
    #         name = name.string
    #     return self.__string.__getattribute__(name=name)

    def __getitem__(self, i: Union[int, slice]) -> str:
        """ Return self[key]. """
        return self.__string.__getitem__(i)

    def __getnewargs__(self):
        pass

    def __ge__(self, x: str) -> bool:
        """ Return self>=value. """
        if isinstance(x, String):
            if self is x:
                return True
            x = x.string
        return self.__string.__ge__(x)

    def __gt__(self, x: str) -> bool:
        """ Return self>value. """
        if isinstance(x, String):
            if self is x:
                return False
            x = x.string
        return self.__string.__gt__(x)

    def __hash__(self) -> int:
        """ Return hash(self). """
        return self.__string.__hash__()

    def __iter__(self) -> Iterator[str]:
        """ Implement iter(self). """
        return self.__string.__iter__()

    def __len__(self) -> int:
        """ Return len(self). """
        return self.__string.__len__()

    def __le__(self, x: str) -> bool:
        """ Return self<=value. """
        if isinstance(x, String):
            if self is x:
                return True
            x = x.string
        return self.__string.__le__(x)

    def __lt__(self, x: str) -> bool:
        """ Return self<value. """
        if isinstance(x, String):
            if self is x:
                return False
            x = x.string
        return self.__string.__lt__(x)

    def __mod__(self, value: Any):
        """ Return self%value. """
        string = self.__string.__mod__(value)
        return String(string=string)

    def __mul__(self, n: int):
        """ Return self*value. """
        string = self.__string.__mul__(n)
        return String(string=string)

    def __ne__(self, x: str) -> bool:
        """ Return self!=value. """
        if isinstance(x, String):
            if self is x:
                return False
            x = x.string
        return self.__string.__ne__(x)

    def __repr__(self) -> str:
        """ Return repr(self). """
        return self.__string

    def __rmod__(self, value: Any):
        """ Return value%self. """
        pass

    def __rmul__(self, n: int):
        """ Return value*self. """
        string = self.__string.__rmul__(n)
        return String(string=string)

    def __sizeof__(self) -> int:
        """ Return the size of the string in memory, in bytes. """
        return self.__string.__sizeof__()

    def __str__(self) -> str:
        """ Return str(self). """
        return self.__string
