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

__all__ = []

try:
    from dc2.core.auth import register_auth_method
    from dc2.core.helpers import hash_generator
except ImportError as e:
    raise e

from ..db.controllers import UsersController


def do_local_authentication(email=None, password=None):
    if email is not None and password is not None:
        ctl_users = UsersController()
        user = ctl_users.get(email=email)
        if user is not None:
            if user.password.password == hash_generator(password):
                return True, user
        return False, None

register_auth_method('local', do_local_authentication)



