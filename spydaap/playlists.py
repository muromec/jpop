#Copyright (C) 2008 Erik Hetzner

#This file is part of Spydaap. Spydaap is free software: you can
#redistribute it and/or modify it under the terms of the GNU General
#Public License as published by the Free Software Foundation, either
#version 3 of the License, or (at your option) any later version.

#Spydaap is distributed in the hope that it will be useful, but
#WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with Spydaap. If not, see <http://www.gnu.org/licenses/>.

import os, time

class Playlist(object):
    name = None
    smart_playlist = True

    def sort(self, entries):
        pass

    def safe_cmp(self, a, b, key):
        if a.has_key(key) and b.has_key(key):
            return cmp(a[key], b[key])
        elif a.has_key(key):
            return 1
        elif b.has_key(key):
            return -1
        else: return 0

    def safe_cmp_series(self, a, b, key_list):
        if len(key_list) == 0:
            return 0
        key = key_list[0]
        r = self.safe_cmp(a, b, key)
        if r != 0:
            return r
        else:
            return self.safe_cmp_series(a, b, key_list[1:])
        
class Library(Playlist):
    def __init__(self):
        self.name = "Library"
        self.smart_playlist = False

    def contains(self, md):
        return True
