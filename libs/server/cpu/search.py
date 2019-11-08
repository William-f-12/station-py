# -*- coding: utf-8 -*-
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
    Command Processor for 'search'
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    search users with keyword(s)
"""

from typing import Optional

from dimp import ID
from dimp import InstantMessage
from dimp import Content
from dimp import Command
from dimsdk import CommandProcessor

from ...common import Database


class SearchCommandProcessor(CommandProcessor):

    @property
    def database(self) -> Database:
        return self.context['database']

    def __search(self, keywords: list) -> Optional[Content]:
        results = self.database.search(keywords=keywords)
        users = list(results.keys())
        response = Command.new(command='search')
        response['message'] = '%d user(s) found' % len(users)
        response['users'] = users
        response['results'] = results
        return response

    def __update(self, content: Content) -> Optional[Content]:
        # TODO: response, update
        pass

    #
    #   main
    #
    def process(self, content: Content, sender: ID, msg: InstantMessage) -> Optional[Content]:
        assert isinstance(content, Command), 'command error: %s' % content
        # message
        message = content.get('message')
        if message is None:
            self.info('search users for %s, %s' % (sender, content))
            keywords = content['keywords'].split(' ')
            return self.__search(keywords=keywords)
        else:
            return self.__update(content=content)


# register
CommandProcessor.register(command='search', processor_class=SearchCommandProcessor)
