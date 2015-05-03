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

try:
    from flask_restful import Resource as RestResource
    from flask_restful.reqparse import RequestParser
    from flask import request
except ImportError as e:
    raise e


try:
    from dc2.core.application import app
    from dc2.core.database import DB
    from dc2.core.helpers import hash_generator
    from dc2.core.auth.decorators import needs_authentication, has_groups
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

_user_list_parser = RequestParser()
_user_list_parser.add_argument('username', type=str, default=None, help="Username", required=False, location="args")
_user_list_parser.add_argument('email', type=str, default=None, help="Email Address", required=False, location="args")

class UserCollection(RestResource):
    def __init__(self, *args, **kwargs):
        super(UserCollection, self).__init__(*args, **kwargs)
        self._ctl_users = UsersController(DB.session)

    @needs_authentication
    @has_groups(['admin'])
    def get(self):
        args = _user_list_parser.parse_args()
        userlist = []
        try:
            if args.username is not None and args.email is None:
                userlist = self._ctl_users.find_by_username(args.username)
            elif args.username is None and args.email is not None:
                userlist = self._ctl_users.find_by_email(args.email)
            else:
                userlist = self._ctl_users.list()
            return [user.to_dict for user in userlist], 200
        except Exception as e:
            app.logger.exception(msg="Exception occured")
            return {'error': True,
                    'message': e.args}, 400

    @needs_authentication
    @has_groups(['admin'])
    def post(self):
        print(request.get_data())
        args = _user_parser.parse_args()
        try:
            user, pw = self._ctl_users.new(**args)
            if user is not None:
                result = {'user': user.to_dict, 'password': pw}
                return result, 201
            else:
                return {'error': True,
                        'message': 'An error occured'}, 400
        except Exception as e:
            app.logger.exception(msg="Exception occured")
            return {'error': True,
                'message': e.args}, 400


class UserRecords(RestResource):

    def __init__(self, *args, **kwargs):
        super(UserRecords, self).__init__(*args, **kwargs)
        self._ctl_users = UsersController(DB.session)

    @needs_authentication
    @has_groups(['admin'])
    def get(self, id=None):
        if id is not None:
            try:
                user = self._ctl_users.get(username=id)
                return user.to_dict, 200
            except Exception as e:
                app.logger.exception(msg="Exception occured")
                return {'error': True, 'message': e.args}, 400
        return {'error': True, 'message': 'No ID or Username'}, 400

    @needs_authentication
    @has_groups(['admin'])
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
                app.logger.exception(msg="Exception occured")
                return {'error': True, 'message': e.args}, 400
        return {'error': True, 'message': 'No ID or Username'}, 400

    @needs_authentication
    @has_groups(['admin'])
    def delete(self, id=None):
        if id is not None:
            try:
                result = self._ctl_users.find_by_username(username=id)
                if result is not None and len(result) > 0:
                    success = self._ctl_users.set_deleted(result[0])
                    return {'status': success}, 200
                result = self._ctl_users.find_by_email(email=id)
                if result is not None and len(result) > 0:
                    success = self._ctl_users.set_deleted(result[0])
                    return {'status': success}, 200
                result = self._ctl_users.find(id=id)
                if result is not None and len(result) > 0:
                    success = self._ctl_users.set_deleted(result[0])
                    return {'status': success}, 200
            except Exception as e:
                app.logger.exception(msg="Exception occured")
                return {'error': True,
                        'message': e.args}, 400
        return {'error': True, 'message': 'No ID or Username'}, 400


class UserEnable(RestResource):
    def __init__(self, *args, **kwargs):
        super(UserEnable, self).__init__(*args, **kwargs)
        self._ctl_users = UsersController(DB.session)

    @needs_authentication
    @has_groups(['admin'])
    def get(self, id=None, state=None):
        if id is not None and state is not None:
            try:
                user = self._ctl_users.get(username=id)
                if user is not None:
                    if state.lower() == 'enable':
                        if self._ctl_users.set_enabled(user):
                            return {'status': True}, 200
                    elif state.lower() == 'disable':
                        if self._ctl_users.set_disabled(user):
                            return {'status': True}, 200
                return {'error': True, 'message': 'Something wrong happened'}, 400
            except Exception as e:
                app.logger.exception(msg="Exception Occured")
                return {'error': True, 'message': e.args}, 400
        return {'error': True, 'message': 'No ID or Username'}, 400

