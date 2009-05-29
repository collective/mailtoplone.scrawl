# -*- coding: utf-8 -*-
#
# File: utilities.py
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

import email

LOGGER="wcms.scrawl"


def info(msg):
    logging.getLogger(LOGGER).info(msg)


def attachments(mail):
    """return a generator which yields dicts like
        { "data": "some text, may also be binary for other files",
          "file_name": "muha.txt"
          "mime_type": "text/plain",
          }
    """
    # we'll make an attachment for every part of the mail which has a
    # filename parameter
    m = email.message_from_string(mail)
    parts = [item for item in m.walk() if item.get_filename() != None]
    for elem in parts:
        charset = elem.get_content_charset() or "ISO-8859-1"
        data = elem.get_payload(decode=1)
        mt= elem.get_content_type().decode(charset).encode("ascii", "ignore")
        fn= elem.get_filename().decode(charset).encode("ascii", "ignore")
        yield dict(
                data=data,
                mime_type=mt,
                file_name=fn,
                )

# vim: set ft=python ts=4 sw=4 expandtab :
