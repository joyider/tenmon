#!/usr/bin/python
# -*- coding: utf-8 -*-
# NoJoy_DI (c) 2016 by Andre Karlsson<andre.karlsson@protractus.se>
#
# This file is part of NoJoy_DI.
#
#    NoJoy_DI is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    NoJoy_DI is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with NoJoy_DI.  If not, see <http://www.gnu.org/licenses/>.
#
# Filename: exceptions by: andrek
# Timesamp: 2016-05-18 :: 14:58

class DIException(Exception):
    """Base exception"""
    pass

class PatternizerException(DIException):

    def __init__(self, s_def, req_tokens):
        last_def = req_tokens[-1]
        super(PatternizerException, self).__init__(
             "Service %s[%s] is requesting %s[%s]. Chain: %s"
             % (last_def.name, last_def._mypattern.__name__, s_def.name, s_def._mypattern.__name__,
                " => ".join([i.name for i in req_tokens])
                )
         )