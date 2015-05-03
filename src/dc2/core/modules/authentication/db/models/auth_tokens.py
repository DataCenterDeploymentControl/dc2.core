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

import sys
import datetime

try:
    from dc2.core.database import DB
except ImportError as e:
    raise e

__author__ = "Stephan Adig <sh@sourcecode.de>"


class AuthToken(DB.Model):
    __tablename__ = 'authtokens'

    id = DB.Column(DB.Integer, primary_key=True)
    token = DB.Column(DB.String, unique=True, nullable=False)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.now())
    is_active = DB.Column(DB.Boolean, default=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    user = DB.relationship('User', uselist=False)

    @property
    def to_dict(self):
        """

        :return: dict
        """
        rec = dict(token=self.token, user=self.user.username)
        return rec
