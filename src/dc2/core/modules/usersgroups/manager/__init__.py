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

__all__ = ['init_seed_commands']

from dc2.core.manager.globals import add_seed_method

from ..db.controllers import UsersController

def seed_initialize_user():
    print('Initialize Users')
    print('Checking for Admin User')
    ctl_user = UsersController()

    admin = ctl_user.get(username='admin')
    print('{0}'.format(admin))
    if admin is None:
        admin = ctl_user.new(username="admin", email="admin@domain.tld", name="Admin User", groups=['admin'])
        print('{0}'.format(admin))
        if admin is not None:
            return True
        return False
    return True

def seed_initialize_groups():
    print('Initialize Groups')
    return False

def init_seed_commands():
    add_seed_method('usersgroups', 'initialize', '01_seed_initialize_user', seed_initialize_user)
    add_seed_method('usersgroups', 'initialize', '02_seed_initialize_group', seed_initialize_groups)

