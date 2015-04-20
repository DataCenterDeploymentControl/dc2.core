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
    raise(e)

import datetime

class User(DB.Model):
    __tablename__ = 'users'

    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String, unique=True, nullable=False)
    email = DB.Column(DB.String, unique=True, nullable=False)
    name = DB.Column(DB.String, nullable=True)
    password = DB.relationship("Password", uselist=False, backref="users", cascade="save-update, merge, delete")
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.now())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.now())
    groups = DB.relationship("Group", secondary='users2groups')

    @property
    def to_dict(self):
        return dict(id=self.id, username=self.username, email=self.email, name=self.name,
                    created_at=self.created_at.isoformat(),
                    updated_at=self.updated_at.isoformat() if self.updated_at is not None else None)
