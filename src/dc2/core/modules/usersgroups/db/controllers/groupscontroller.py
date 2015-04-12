# -*- coding: utf-8 -*-
#
#
# (DC)² - DataCenter Deployment Control
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
    raise e

from dc2.core.database.controllers import BaseController
from ..models import Group


class GroupsController(BaseController):

    def list(self):
        try:
            result = self._session.query(Group).all()
            return result
        except Exception as e:
            print(e)
            return None


    def find(self, *args, **kwargs):
        if 'id' not in kwargs and 'groupname' not in kwargs:
            raise ValueError('id or groupnmae need to be given')
        try:
            groups = self._session.query(Group).filter_by(**kwargs).all()
            return groups
        except Exception as e:
            print(e)
            return None

    def find_by_id(self, id=None):
        if id is not None and isinstance(id, int):
            return self.find(id=id)
        return None

    def find_by_groupname(self, groupname=None):
        if groupname is not None and isinstance(groupname, str):
            return self.find(groupname=groupname)
        return None

    def find_in_groupnames(self, groupname=None):
        if groupnames is not None and isinstance(groupnames, list):
            try:
                result = Group.query.filter(Group.groupname.in_(groupnames)).all()
                return result
            except Exception as e:
                print(e)
                return None
        return None

    def get(self, *args, **kwargs):
        if 'groupname' in kwargs:
            try:
                group = self._session.query(Group).filter_by(groupname=kwargs['groupname']).first()
                return group
            except Exception as e:
                print(e)
                return None
        return None

    def new(self, *args, **kwargs):
        group = Group(**kwargs)
        try:
            record = self.add(group)
            return record
        except Exception as e:
            print(e)
            return None

    def _add_or_update(self, record=None):
        try:
            if record is not None:
                self._session.add(record)
                self._session.commit()
                return record
        except IntegrityError as e:
            print(e)
            return None

    def delete(self, record=None):
        try:
            if record is not None:
                self._session.delete(record)
                self._session.commit()
                return True
        except Exception as e:
            print(e)
            return False



