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
import sys

try:
    from flask_restful import Resource as RestResource
    from flask_restful.reqparse import RequestParser
except ImportError as e:
    raise e


try:
    from dc2.core.database import DB
    from dc2.core.helpers import hash_generator
    from dc2.core.auth.decorators import needs_authentication, has_groups
except ImportError as e:
    raise e

try:
    from ...db.controllers import GroupsController
except ImportError as e:
    raise e

_group_parser = RequestParser()
_group_parser.add_argument('groupname', type=str, help="Groupname", required=True, location="json")
_group_parser.add_argument('desc', type=str, help="Description", required=False, default="No Description", location="json")

_group_find_parser = RequestParser()
_group_find_parser.add_argument('groupname', type=str, default=None, help="Groupname", required=False, location="args")


class GroupCollection(RestResource):
    def __init__(self, *args, **kwargs):
        super(GroupCollection, self).__init__(*args, **kwargs)
        self._ctl_groups = GroupsController()

    @needs_authentication
    @has_groups(['admin'])
    def get(self):
        args = _group_find_parser.parse_args()
        groupslist = []
        if args.groupname is None:
            groupslist = self._ctl_groups.list()
        else:
            groupslist = self._ctl_groups.find_by_groupname(groupname=args.groupname)
        return [group.to_dict for group in groupslist], 200

    @needs_authentication
    @has_groups(['admin'])
    def post(self):
        args = _group_parser.parse_args()
        try:
            group = self._ctl_groups.new(args.groupname, args.desc)
            if group is not None:
                result = {'group': group.to_dict}
                return result, 201
            return {'error': True, 'message': 'Something went wrong'}, 404
        except Exception as e:
            # TODO: Change to logger
            print(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
            return {'error': True, 'message': e}, 404


class GroupRecords(RestResource):
    def __init__(self, *args, **kwargs):
        super(GroupRecords, self).__init__(*args, **kwargs)
        self._ctl_groups = GroupsController()

    @needs_authentication
    @has_groups(['admin'])
    def get(self, groupname=None):
        if groupname is not None:
            try:
                group = self._ctl_groups.get(groupname=groupname)
                return group.to_dict, 200
            except Exception as e:
                # TODO: Change to logger
                print(e)
                return None, 404
        return None, 404

    @needs_authentication
    @has_groups(['admin'])
    def put(self, groupname=None):
        if groupname is not None:
            args = _group_parser.parse_args()
            try:
                group = self._ctl_groups.get(groupname=groupname)
                group.descr = args.desc
                self._ctl_groups.update(group)
                return group.to_dict, 200
            except Exception as e:
                # TODO: Change to logger
                print(e)
                return None, 404
        return None, 404

    @needs_authentication
    @has_groups(['admin'])
    def delete(self, groupname=None):
        if groupname is not None:
            try:
                group = self._ctl_groups.get(groupname=groupname)
                if group is not None:
                    self._ctl_groups.delete(group)
                    return True, 200
                else:
                    return None, 404
            except Exception as e:
                # TODO: Change to logger
                print(e)
                return None, 404
        return None, 404
