# -*- coding: utf-8 -*-
#
# File: interfaces.py
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


from zope.interface import Interface
from mailtoplone.base.interfaces import IMailDropBoxMarker

class IScrawlMailDropBoxMarker(IMailDropBoxMarker):
    """ marker interface for Scrawl mail drop boxes """

class IBlogEntryFactory(Interface):
    """ create a Blog Entry

    To create a blog entry use::

        >>> factory = queryMultiAdapter((context, request), IBlogEntryFactory, default=Default(context, request))
        >>> factory.add_category("email")
        >>> factory.add_category("foo")
        >>> factory.add_file("filedata", "text/plain", "sometext.txt")
        >>> factory.add_file(imgdata, "image/jpeg", "foo.jpg")
        >>> entry = factory.create("Some silly subject", "hey there, this is my text")

    """
    def create(title, text):
        """ create the Blog Entry on the context and return it"""

    def add_file(data, name, mime_type):
        """ add a file to the Blog Entry """

    def add_category(category):
        """ add a category """

# vim: set ft=python ts=4 sw=4 expandtab :
