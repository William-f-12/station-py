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
    Document Command Processor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from typing import Optional

from dimp import ID, Meta, Document
from dimp import ReliableMessage
from dimp import Content, TextContent
from dimp import Command, DocumentCommand

from ..protocol import ReceiptCommand

from .command import CommandProcessor


class DocumentCommandProcessor(CommandProcessor):

    def __get(self, identifier: ID, doc_type: str='*') -> Content:
        facebook = self.facebook
        # query entity document for ID
        doc = facebook.document(identifier=identifier, doc_type=doc_type)
        if facebook.is_empty_document(document=doc):
            # document not found
            text = 'Sorry, document not found for ID: %s' % identifier
            return TextContent(text=text)
        # response
        meta: Meta = facebook.meta(identifier=identifier)
        return DocumentCommand.response(document=doc, meta=meta, identifier=identifier)

    def __put(self, identifier: ID, meta: Meta, document: Document) -> Content:
        facebook = self.facebook
        if meta is not None:
            # received a meta for ID
            if not facebook.save_meta(meta=meta, identifier=identifier):
                # save meta failed
                text = 'Meta not accept: %s!' % identifier
                return TextContent(text=text)
        # received a new document for ID
        if not facebook.save_document(document=document):
            # save document failed
            text = 'Document not accept: %s!' % identifier
            return TextContent(text=text)
        # response
        text = 'Document received: %s' % identifier
        return ReceiptCommand(message=text)

    def execute(self, cmd: Command, msg: ReliableMessage) -> Optional[Content]:
        assert isinstance(cmd, DocumentCommand), 'command error: %s' % cmd
        identifier = cmd.identifier
        doc = cmd.document
        if doc is None:
            doc_type = cmd.get('doc_type')
            if doc_type is None:
                doc_type = '*'
            return self.__get(identifier=identifier, doc_type=doc_type)
        else:
            # check meta
            meta = cmd.meta
            return self.__put(identifier=identifier, meta=meta, document=doc)
