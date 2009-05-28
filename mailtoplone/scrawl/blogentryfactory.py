# -*- coding: utf-8 -*-
#
# File: blogentryfactory.py
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

__author__ = """Hans-Peter Locher <hans-peter.locher@inquant.de>"""
__docformat__ = 'plaintext'


import logging

from Acquisition import aq_base

from zope import interface
from zope import component
from zope.event import notify

from zope.app.container.interfaces import INameChooser
from plone.i18n.normalizer.interfaces import IIDNormalizer

from mailtoplone.base.events import MailDroppedEvent

from mailtoplone.scrawl.interfaces import IBlogEntryFactory

LOGGER="wcms.scrawl"


def info(msg):
    logging.getLogger(LOGGER).info(msg)


class BlogEntryFactory(object):
    """ create a Blog Entry

    To create a blog entry use::

        >>> factory = queryMultiAdapter((context, request), IBlogEntryFactory, default=Default(context, request))
        >>> factory.add_category("email")
        >>> factory.add_category("foo")
        >>> factory.add_file("filedata", "text/plain", "sometext.txt")
        >>> factory.add_file(imgdata, "image/jpeg", "foo.jpg")
        >>> entry = factory.create("Some silly subject", "hey there, this is my text")

    """
    interface.implements(IBlogEntryFactory)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def create(self, title, text):
        """ create the Blog Entry on the context and return it"""

        normalizer = component.getUtility(IIDNormalizer)
        chooser = INameChooser(self.context)
        id = chooser.chooseName(normalizer.normalize(title), aq_base(self.context))

        self.context.invokeFactory(
                'Blog Entry',
                id=id,
                title=title,
                text=text)

        blog_entry = getattr(self.context, id)
        blog_entry.processForm()
        notify(MailDroppedEvent(blog_entry, self.context))
        return blog_entry

    def add_file(self, data, name, mime_type):
        """ add a file to the Blog Entry """
        pass

    def add_category(self, category):
        """ add a category """
        pass



# vim: set ft=python ts=4 sw=4 expandtab :
