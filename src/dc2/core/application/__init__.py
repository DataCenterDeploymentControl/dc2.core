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
from ..helpers import init_logger

def init_application(app, manager=None):
    global app_cache
    app.config.from_envvar("DC2_CONFIGURATION")
    init_db(app)
    handler = None
    if 'LOGFILE' in app.config:
        handler = init_logger(app.config['LOGFILE'])
    else:
        handler = init_logger('application.log')
    if handler is not None:
        app.logger.addHandler(handler)

    if 'RUN_VIA_MANAGER' in app.config and app.config['RUN_VIA_MANAGER'] and manager is not None:
        # import Manager applications
        for module in app.config['MODULES']:
            if 'enabled' in module and module['enabled']:
                try:
                    mod = importlib.import_module(module['module'])
                    mod.init_manager_commands(manager)
                except Exception as e:
                    raise e
    else:
        if app_cache is None:
            app_cache = init_app_cache(app.config['MEMCACHE_SERVERS'], app.config['DEBUG'])
            app.config['app_cache'] = app_cache
            print('init app_cache')

        for authenticator in app.config['AUTHENTICATORS']:
            importlib.import_module(authenticator)

        for module in app.config['MODULES']:
            print(module)
            if 'enabled' in module and module['enabled']:
                try:
                    mod = importlib.import_module(module['module'])

                    for prefix in module['url_prefix']:
                        bp = mod.init_blueprint(prefix)
                        app.register_blueprint(bp, url_prefix="{0}{1}".format(app.config['API_PREFIX'], prefix['prefix']))
                except Exception as e:
                    raise e
        print(app.url_map)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-DC2-Auth-Token,X-DC2-Auth-User')
    response.headers.add('Access-Control-Allow-Methods', '  GET,PUT,POST,DELETE')
    response.headers.add('Access-Control-Expose-Headers', 'X-DC2-Auth-Token,X-DC2-Auth-User')
    return response

