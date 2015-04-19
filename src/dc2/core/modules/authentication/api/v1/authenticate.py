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
    from dc2.core.database import DB
    from dc2.core.cache import app_cache
    from dc2.core.auth import AUTH_TYPES, AUTH_TYPE_METHODS
except ImportError as e:
    raise e

try:
    from flask import request
    from flask_restful import Resource as RestResource
    from flask_restful.reqparse import RequestParser
    from flask_restful.inputs import boolean
except ImportError as e:
    raise (e)

from dc2.core.modules.authentication.db.controllers import AuthTokenController

_auth_parser = RequestParser()
_auth_parser.add_argument('email', type=str, required=True, location='json', help="email")
_auth_parser.add_argument('password', type=str, required=True, location='json', help="password")
_auth_parser.add_argument('auth_type', type=str, required=True, default='local', location='json', help='auth+type')


class Authenticate(RestResource):
    def __init__(self, *args, **kwargs):
        super(Authenticate, self).__init__(*args, **kwargs)
        self._ctl_auth = AuthTokenController()

    def post(self):
        args = _auth_parser.parse_args()
        try:
            if args.auth_type.lower() in AUTH_TYPES:
                is_authenticated, user = AUTH_TYPE_METHODS[args.auth_type.lower()]['authfunc'](args)
                if is_authenticated:
                    old_token = self._ctl_auth.find(user=user)
                    if old_token is not None:
                        old_token.is_active = False
                        self._ctl_auth.update(old_token)
                        if app_cache.get(old_token.token) is not None:
                            app_cache.delete(old_token.token)
                    token = self._ctl_auth.new(is_authenticated=is_authenticated, user=user, ip=request.remote_addr)
                    if app_cache.get(token.token) is None:
                        app_cache.set(token.token, {
                            'is_authenticated': is_authenticated,
                            'user': user.to_dict}, 5 * 60)
                    return {
                        'authenticated': is_authenticated,
                        'user': user.to_dict
                    }, 200, {'X-DC2-Auth-Token': token.token,
                             'X-DC2-Auth-User': user.username}
        except Exception as e:
            # TODO: Change to logger
            print(e)
            return None, 404
