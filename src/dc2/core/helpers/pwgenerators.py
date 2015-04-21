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

import string
import random
from hashlib import sha512

__all__ = ['pw_generator', 'hash_generator']


def pw_generator(size=8, chars=string.ascii_uppercase+string.ascii_lowercase+string.digits):
    """

    :param size: int
    :param chars: string (defaults to string.ascii_uppercase+string.ascii_lowercase+string.digits
    :return: (pwstring, sha512 hexdigest string)

    """
    pw = ''.join(random.SystemRandom().choice(chars) for _ in range(size))
    return pw, hash_generator(pw)


def hash_generator(text=None):
    """

    :param text: string
    :return: hexdigest string
    """
    if text is None:
        raise ValueError('text can not be None')
    if not isinstance(text, str):
        raise ValueError('text needs to be an instance of str')
    sha512hash = sha512()
    sha512hash.update(text.encode('ascii'))
    return sha512hash.hexdigest()