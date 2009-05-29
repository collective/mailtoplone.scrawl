# -*- coding: utf-8 -*-
#
# File: adapter.py
#
# Copyright (c) InQuant GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__    = """Hans-Peter Locher<hans-peter.locher@inquant.de>"""
__docformat__ = 'plaintext'

import email
import logging

from zope import interface
from zope import component

from mailtoplone.base.interfaces import IMailDropBox
from mailtoplone.base.interfaces import IBodyFactory

from mailtoplone.base.browser.emailview import EmailView

from mailtoplone.scrawl.interfaces import IBlogEntryFactory
from mailtoplone.scrawl.blogentryfactory import BlogEntryFactory

info = logging.getLogger().info


class ScrawlMailDropBox(object):
    """ adapts IScrawlMailDropBoxmarker to a IMailDropBox """

    interface.implements(IMailDropBox)

    def __init__(self, context):
        self.context = context

    def drop(self, mail):
        """ drop a mail into this mail box. The mail is
        a string with the complete email content """
        body_factory = component.queryUtility(IBodyFactory)
        email_view = EmailView(self.context, None)


        # get the body and matching content_type, charset
        body, content_type, charset = body_factory(mail)

        mailobj = email.message_from_string(mail)

        # Subject
        for key in "Subject subject Betreff x-blog-title".split():
            subject = mailobj.get(key)
            if subject is not None:
                break

        #decode subject
        subject = email_view.decodeheader(subject)

        factory = component.queryMultiAdapter((self.context, None),\
                IBlogEntryFactory,\
                default=BlogEntryFactory(self.context, None))

        factory.create(subject, body)



# vim: set ft=python ts=4 sw=4 expandtab :
