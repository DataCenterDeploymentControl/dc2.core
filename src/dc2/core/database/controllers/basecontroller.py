# -*- coding: utf-8 -*-
#
#
# DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

__author__ = 'stephan.adig'

try:
    from sqlalchemy.exc import IntegrityError
except ImportError as e:
    raise(e)


from ..base import DB


class BaseController(object):

    def __init__(self, session=None):
        self._session = DB.session
        if session is not None:
            self._session = session

    def list(self):
        pass

    def find(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        pass

    def new(self, *args, **kwargs):
        pass

    def _add_or_update(self, record=None):
        try:
            if record is not None:
                self._session.add(record)
                self._session.commit()
                return record
        except IntegrityError as e:
            raise e

    def add(self, record=None):
        result = self._add_or_update(record)
        return result

    def update(self, record=None):
        result = self._add_or_update(record)
        return result

    def delete(self, record=None):
        pass

