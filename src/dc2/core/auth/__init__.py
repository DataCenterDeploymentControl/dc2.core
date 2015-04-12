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

__all__ = ["AUTH_TYPES", "AUTH_TYPE_METHODS", 'register_auth_method']

from .auth_types import AUTH_TYPES, AUTH_TYPE_METHODS


def register_auth_method(auth_name=None, auth_method_func=None):
    if auth_name is not None and auth_method_func is not None:
        if auth_name not in AUTH_TYPES:
            AUTH_TYPES.append(auth_name)

        if auth_name not in AUTH_TYPE_METHODS.keys():
            AUTH_TYPE_METHODS.append(
                {
                    auth_name: {'authfunc': auth_method_func}
                }
            )
