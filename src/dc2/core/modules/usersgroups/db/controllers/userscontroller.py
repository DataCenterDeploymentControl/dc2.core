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
import sys

try:
    from sqlalchemy.exc import IntegrityError
except ImportError as e:
    raise e

from dc2.core.application import app
from dc2.core.helpers import pw_generator, hash_generator
from dc2.core.database.controllers import BaseController
from ..controllers import GroupsController
from ..models import User
from ..models import Password


class UsersController(BaseController):

    def __init__(self, session=None):
        super(UsersController, self).__init__(session)
        self._ctl_groups = GroupsController(self._session)

    def list(self):
        try:
            result = User.query.all()
            return result
        except Exception as e:
            print(e)
            return None

    def find_by_username(self, username=None):
        if username is not None:
            try:
                result = User.query.filter_by(username=username).all()
                return result
            except Exception as e:
                print(e)
                return None
        return None

    def find_by_email(self, email=None):
        if email is not None:
            try:
                result = User.query.filter_by(email=email).all()
                return result
            except Exception as e:
                print(e)
                return None
        return None

    def new(self, username=None, name=None, email=None, password=None, groups=[]):
        try:
            pw = None
            grps = None
            if password is not None:
                pw = password
            if groups is not None and isinstance(groups, list) and len(groups) > 0:
                grps = groups
            record = User(username=username, name=name, email=email)
            if pw is not None:
                pw_rec = Password(password=hash_generator(pw))
                record.password = pw_rec
            else:
                pw, hashstring = pw_generator(size=12)
                record.password = Password(password=hashstring)
            if grps is not None and isinstance(grps, list):
                groups_record = self._ctl_groups.find_in_groupnames(grps)
                if groups_record is None:
                    return None, None
                record.groups = groups_record
            try:
                record = self.add(record)
                return record, pw
            except Exception as e:
                print(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
                return None, None
        except Exception as e:
            print(e)
            return None, None

    def get(self, *args, **kwargs):
        if 'username' in kwargs or 'email' in kwargs or 'id' in kwargs:
            user = User.query.filter_by(**kwargs).first()
            return user
        return None

    def add_groups(self, user=None, groupnames=None):
        if user is not None and groupnames is not None and isinstance(groupnames, list):
            groups = self._ctl_groups.find_in_groupnames(groupnames)
            print(groups)
            user.groups = groups
            return user
        return None

    def set_deleted(self, record=None):
        if record is not None:
            try:
                record.is_deleted = True
                self._session.commit()
            except Exception as e:
                app.logger.exception(msg='Exception Occured')
                return {'error':True, 'message': e.args}, 400
        return {'error':True, 'message': 'Record was none'}, 400

    def set_enabled(self, record=None):
        if record is not None:
            try:
                record.is_deleted = False
                self._session.commit()
                return True
            except Exception as e:
                app.logger.exception(msg="Exception Occured")
                return False
        return False

    def set_disabled(self, record=None):
        if record is not None:
            try:
                record.is_deleted = True
                self._session.commit()
                return True
            except Exception as e:
                app.logger.exception(msg="Exception occured")
                return False
        return False

    def delete(self, record=None):
        if record is not None:
            try:
                # record.is_deleted = True
                self._session.delete(record)
                self._session.commit()
                return True
            except Exception as e:
                app.logger.exception(msg="Exception occured")
                return False
        return False