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

__all__ = ['needs_authentication', 'has_group']


from functools import wraps

from flask import g

def needs_authentication(f):
    try:
        from flask import request
        from flask_restful import abort
    except ImportError as e:
        raise e

    from ...application import app_cache

    @wraps(f)
    def wrapped(*args, **kwargs):
        if g.get('auth_user', None) is None and g.get('auth_token', None) is None:
            auth_token = request.headers.get('X-DC2-Auth-Token')
            auth_user = request.headers.get('X-DC2-Auth-User')
            if auth_token is not None:
                cache_token = app_cache.get(auth_token)
                if (cache_token is not None and 'is_authenticated' in cache_token
                    and cache_token['is_authenticated']
                    and 'user' in cache_token
                    and 'username' in cache_token['user']):
                    if cache_token['user']['username'] == auth_user:
                        app_cache.set(auth_token, cache_token, 5 * 60)
                        g.auth_user = auth_user
                        g.auth_token = auth_token
                        return f(*args, **kwargs)
            abort(401)
        else:
            cache_token = app_cache.get(g.auth_token)
            if cache_token is None:
                del g.auth_token
                del g.auth_user
                abort(401)
            app_cache.set(auth_token, cache_token, 5 * 60)
    return wrapped


def has_groups(groupnames=[]):
    def has_groups_decorator(f):
        try:
            from flask import request
            from flask_restful import abort
        except ImportError as e:
            raise e

        from ...application import app_cache

        @wraps(f)
        def wrapped(*args, **kwargs):
            auth_token = request.headers.get('X-DC2-Auth-Token')
            auth_user = request.headers.get('X-DC2-Auth-User')
            if auth_token is not None:
                cache_token = app_cache.get(auth_token)
                if (cache_token is not None and 'is_authenticated' in cache_token
                    and cache_token['is_authenticated']
                    and 'user' in cache_token
                    and 'username' in cache_token['user']):
                    if cache_token['user']['username'] == auth_user:
                        if 'groups' in cache_token['user']:
                            for usergroup in cache_token['user']['groups']:
                                if usergroup in groupnames:
                                    return f(*args, **kwargs)
            abort(401)
        return wrapped
    return has_groups_decorator