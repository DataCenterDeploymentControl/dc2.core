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

__all__ = ['AuthTokenController']

import datetime
import hashlib

try:
    from sqlalchemy.exc import IntegrityError
except ImportError as e:
    raise e

try:
    from dc2.core.database import DB
    from dc2.core.database.controllers import BaseController
    from dc2.core.modules.usersgroups.db.controllers import UsersController
    from dc2.core.helpers.pwgenerators import hash_generator
except ImportError as e:
    raise e

from ..models import AuthToken

class AuthTokenController(BaseController):
    def __init__(self, session=None):
        self._session = DB.session
        if session is not None:
            self._session = session
        self._ctl_users = UsersController()

    def find(self, user=None):
        if user is None:
            raise ValueError('user can not be None')
        try:
            result = AuthToken.query.filter_by(user=user, is_active=True).first()
            return result
        except Exception as e:
            # TODO; Change to Logger
            print(e)
            return None

    def new(self, is_authenticated=False, user=None, ip=None):
        try:
            if is_authenticated and user is not None and ip is not None:
                token = AuthToken()
                token.user = user
                token.token = hash_generator('{0}:{1}:{2}'.format(user.username, ip, datetime.datetime.now().isoformat()))
                token.is_active = True
                token = self.add(token)
                return token
        except Exception as e:
            # TODO: Change to Logger
            print(e)
            return None
