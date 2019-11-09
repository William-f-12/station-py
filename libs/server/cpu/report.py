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
    Command Processor for 'report'
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Report protocol
"""

from typing import Optional

from dimp import ID
from dimp import InstantMessage
from dimp import Content
from dimp import Command
from dimsdk import Session
from dimsdk import ReceiptCommand
from dimsdk import CommandProcessor

from ...common import Database
from ...common import Messenger


class ReportCommandProcessor(CommandProcessor):

    @property
    def messenger(self) -> Messenger:
        return super().messenger

    @property
    def database(self) -> Database:
        return self.context['database']

    @property
    def receptionist(self):
        return self.context['receptionist']

    def __process_old_report(self, cmd: Command, sender: ID) -> Optional[Content]:
        # compatible with v1.0
        state = cmd.get('state')
        self.info('client report state %s' % state)
        if state is not None:
            session = self.messenger.current_session(identifier=sender)
            if 'background' == state:
                session.active = False
            elif 'foreground' == state:
                # welcome back!
                self.receptionist.add_guest(identifier=session.identifier)
                session.active = True
            else:
                self.error('unknown state %s' % state)
                session.active = True
            return ReceiptCommand.new(message='Client state received')
        self.error('report info error: %s' % cmd)

    #
    #   main
    #
    def process(self, content: Content, sender: ID, msg: InstantMessage) -> Optional[Content]:
        assert isinstance(content, Command), 'command error: %s' % content
        self.info('client broadcast %s, %s' % (sender, content))
        # report title
        title = content.get('title')
        if 'report' == title:
            return self.__process_old_report(cmd=content, sender=sender)
        # get CPU by report title
        cpu = self.cpu(command=title)
        # check and run
        if cpu is None:
            self.error('command not supported yet: %s' % content)
        elif cpu is self:
            # FIXME: dead cycle!
            self.error('Dead cycle! command: %s' % content)
            raise AssertionError('Dead cycle!')
        else:
            # process by subclass
            return cpu.process(content=content, sender=sender, msg=msg)


class APNsCommandProcessor(ReportCommandProcessor):

    #
    #   main
    #
    def process(self, content: Content, sender: ID, msg: InstantMessage) -> Optional[Content]:
        assert isinstance(content, Command), 'command error: %s' % content
        # submit device token for APNs
        token = content.get('device_token')
        self.info('client report token %s' % token)
        if token is not None:
            self.database.save_device_token(token=token, identifier=sender)
            return ReceiptCommand.new(message='Token received')


class OnlineCommandProcessor(ReportCommandProcessor):

    #
    #   main
    #
    def process(self, content: Content, sender: ID, msg: InstantMessage) -> Optional[Content]:
        assert isinstance(content, Command), 'command error: %s' % content
        # welcome back!
        self.info('client online')
        self.receptionist.add_guest(identifier=sender)
        session = self.messenger.current_session(identifier=sender)
        if isinstance(session, Session):
            session.active = True
        return ReceiptCommand.new(message='Client online received')


class OfflineCommandProcessor(ReportCommandProcessor):

    #
    #   main
    #
    def process(self, content: Content, sender: ID, msg: InstantMessage) -> Optional[Content]:
        assert isinstance(content, Command), 'command error: %s' % content
        # goodbye!
        self.info('client offline')
        session = self.messenger.current_session(identifier=sender)
        if isinstance(session, Session):
            session.active = False
        return ReceiptCommand.new(message='Client offline received')


# register
CommandProcessor.register(command='report', processor_class=ReportCommandProcessor)
CommandProcessor.register(command='broadcast', processor_class=ReportCommandProcessor)

CommandProcessor.register(command='apns', processor_class=APNsCommandProcessor)
CommandProcessor.register(command='online', processor_class=OnlineCommandProcessor)
CommandProcessor.register(command='offline', processor_class=OfflineCommandProcessor)
