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

from . import manager
from .globals import SEED_METHODS


@manager.command
@manager.option('-i', '--initialize', dest='initialize', default=False)
@manager.option('-u', '--upgrade', dest='upgrade', default=False)
@manager.option('-d', '--downgrade', dest='downgrade', default=False)
def seed(initialize=False, upgrade=False, downgrade=False):
    for seed in SEED_METHODS.keys():
        if initialize:
            for method in sorted(SEED_METHODS[seed]['initialize'].keys()):
                if not SEED_METHODS[seed]['initialize'][method]():
                    print('Something went wrong in {0}: {1} ==> {2}'.format(seed, 'initialize', method))
        elif upgrade:
            for method in SEED_METHODS[seed]['upgrade'].keys():
                if not SEED_METHODS[seed]['upgrade'][method]():
                    print('Something went wrong in {0}: {1} ==> {2}'.format(seed, 'upgrade', method))
        elif downgrade:
            for method in SEED_METHODS[seed]['downgrade'].keys():
                if not SEED_METHODS[seed]['downgrade'][method]():
                    print('Something went wrong in {0}: {1} ==> {2}'.format(seed, 'downgrade', method))





