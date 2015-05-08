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
    from psycopg2.errorcodes import lookup as psql_lookup
except ImportError as e:
    raise e

from .exceptions import *

SQL_ERROR_TRANSLATION = {
    'UNIQUE_VIOLATION': UniqueViolationsExceptions
}


def lookup_error(engine='postgres', exc=None):
    if exc is None:

        raise ValueError('exc can not be None')
    if engine.lower() == 'postgres':
        error_name = psql_lookup(exc.orig.pgerror)
        if error_name in SQL_ERROR_TRANSLATION:
            return SQL_ERROR_TRANSLATION[error_name](error_name, exc.orig.diag.message_primary)

    elif engine.lower() == 'mysql':
        return 'not implemented'
    else:
        return 'Unknown Engine'

