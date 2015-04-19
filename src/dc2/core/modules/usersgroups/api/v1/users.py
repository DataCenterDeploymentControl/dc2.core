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
    from flask_restful import Resource as RestResource
    from flask_restful.reqparse import RequestParser
except ImportError as e:
    raise e


try:
    from dc2.core.database import DB
    from dc2.core.helpers import hash_generator
    from dc2.core.auth.decorators import needs_authentication
except ImportError as e:
    raise e

try:
    from ...db.controllers import UsersController
except ImportError as e:
    raise e

_user_parser = RequestParser()
_user_parser.add_argument('username', type=str, help="Username", required=True, location="json")
_user_parser.add_argument('email', type=str, help="EMail Address", required=True, location="json")
_user_parser.add_argument('name', type=str, help="Name", default="No Name", required=False, location="json")
_user_parser.add_argument('password', type=str, help="Password", default=None, required=False, location="json")
_user_parser.add_argument('groups', type=list, help="Groupnames", default=None, required=False, location="json")


class UserCollection(RestResource):
    def __init__(self, *args, **kwargs):
        super(UserCollection, self).__init__(*args, **kwargs)
        self._ctl_users = UsersController(DB.session)

    def get(self):
        userlist = self._ctl_users.list()
        return [user.to_dict for user in userlist], 200

    def post(self):
        args = _user_parser.parse_args()
        user, pw = self._ctl_users.new(**args)
        result = {'user': user.to_dict, 'password': pw}
        return result, 201


class UserRecords(RestResource):

    def __init__(self, *args, **kwargs):
        super(UserRecords, self).__init__(*args, **kwargs)
        self._ctl_users = UsersController()

    def get(selfself, id=None):
        if id is not None:
            try:
                user = self._ctl_users.get(username=id)
                return user.to_dict, 200
            except Exception as e:
                print(e)
                return {'error': True, 'message': e}, 400
        return {'error': True, 'message': 'No ID or Username'}, 400

    def put(self, id=None):
        if id is not None:
            args = _user_parser.parse_args()
            try:
                user = self._ctl_users.get(username=id)
                user.name = args.name
                if args.password is not None:
                    user.password.password = hash_generator(args.password)
                if args.groups is not None and isinstance(args.groups, list):
                    user = self._ctl_users.add_groups(user, args.groups)
                self._ctl_users.update(user)
                return user.to_dict, 200
            except Exception as e:
                print(e)
                return {'error': True, 'message': e}, 400
        return {'error': True, 'message': 'No ID or Username'}, 400

    def delete(self, id=None):
        if id is not None:
            return {}, 200
        return {'error': True, 'message': 'No ID or Username'}, 400




