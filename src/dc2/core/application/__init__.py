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

__author__ = 'Stephan Adig <sh@sourcecode.de>'

import importlib

try:
    from flask import Flask
except ImportError as e:
    raise(e)

__all__ = ['app', 'init_application', 'app_cache']

app = Flask(__name__)

from ..database import init_db
from ..cache import init_app_cache, app_cache


def init_application(app):
    global app_cache
    init_db(app)
    if app_cache is None:
        app_cache = init_app_cache(app.config['MEMCACHE_SERVERS'], app.config['DEBUG'])

    for authenticator in app.config['AUTHENTICATORS']:
        importlib.import_module(authenticator)

    for module in app.config['MODULES']:
        if 'enabled' in module and module['enabled']:
            mod = importlib.import_module(module['module'])
            for prefix in module['url_prefix']:
                bp = mod.init_blueprint(prefix)
                app.register_blueprint(bp, url_prefix="{0}{1}".format(app.config['API_PREFIX'], prefix['prefix']))
    print(app.url_map)


