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

__all__ = ['SEED_METHODS', 'add_seed_method']

SEED_METHODS = {}

FLAGS = [
    'initialize',
    'upgrade',
    'downgrade'
]

def add_seed_method(name=None, flag=None, method_name=None, method=None):
    if name is not None and method_name is not None and method is not None and flag is not None:
        if name not in SEED_METHODS.keys():
            SEED_METHODS[name] = {}
        if flag.lower() in FLAGS:
            if flag.lower() not in SEED_METHODS[name]:
                SEED_METHODS[name][flag.lower()] = {}

            if method_name not in SEED_METHODS[name][flag.lower()].keys():
                SEED_METHODS[name][flag.lower()].update({method_name: method})

