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

import mutagen, re, spydaap, re, os, sys

class VorbisParser(spydaap.parser.Parser):
    MAP = {
      'grouping' : ('grouping','s'),
      'title'    : ('name','s'),
      'artist'   : ('artist','s'),
      'composer' : ('composer','s'),
      'genre'    : ('genre','s'),
      'album'    : ('album','s'),
      'albumartist': ('albumartist','s'),

      'bpm'         : ('beatsperminute','i'),
      'date'        : ('year','i'),
      'year'        : ('year','i'),
      'compilation' : ('compilation','i'),
    }

    file_re = re.compile(".*\\.([fF][lL][aA][cC]|[oO][gG]{2})$")
    def understands(self, filename):
        return self.file_re.match(filename)

    def parser_get(self, filename):
      return mutagen.File(filename)
