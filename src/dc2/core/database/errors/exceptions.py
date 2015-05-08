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

__all__ = ['UniqueViolationsExceptions']

class UniqueViolationsExceptions(Exception):
    def __init__(self, error_code, error_message):
        self._error_code = error_code
        self._error_message = error_message

    def __str__(self):
        return repr('{0}: {1}'.format(self._error_code, self._error_message))

    @property
    def error_message(self):
        return self._error_message

    @property
    def error_code(self):
        return self._error_code
