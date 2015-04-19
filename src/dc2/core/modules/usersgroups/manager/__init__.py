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

from dc2.core.manager.globals import add_seed_method


def seed_initialize_user():
    print('Initialize Users')
    return True
def seed_initialize_groups():
    print('Initialize Groups')
    return False

def init_seed_commands():
    add_seed_method('usersgroups', 'initialize', 'seed_initialize_user', seed_initialize_user)
    add_seed_method('usersgroups', 'initialize', 'seed_initialize_group', seed_initialize_groups)

