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
except ImportError as e:
    raise e

import datetime

class Group(DB.Model):
    __tablename__ = 'groups'

    id = DB.Column(DB.Integer, primary_key=True)
    groupname = DB.Column(DB.String, unique=True, nullable=False)
    descr = DB.Column(DB.String, nullable=True)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.now())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.now())

    @property
    def to_dict(self):
        return dict(id=self.id, groupname=self.groupname, descr=self.descr if self.descr is not None else None,
                    created_at=self.created_at.isoformat(),
                    updated_at=self.updated_at.isoformat() if self.updated_at is not None else None)
