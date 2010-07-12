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

import mutagen.id3, mutagen.mp3, re, spydaap, re, os, struct, sys
mutagen.id3.ID3.PEDANTIC = False
import logging

class Mp3Parser(spydaap.parser.Parser):
    MAP = {
      'TIT1': ('grouping','s'),
      'TIT2': ('name','s'),
      'TPE1': ('artist','s'),
      'TPE3': ('albumartist','s'),
      'TCOM': ('composer','s'),
      'TCON': ('genre','s'),
      'TALB': ('album','s'),
      'TBPM': ('beatsperminute','i'),
      'TDRC': ('year','i'),
      'TCMP': ('compilation','i'),
    }

    file_re = re.compile(".*\\.[mM][pP]3$")
    def understands(self, filename):
      return self.file_re.match(filename)

    def parser_get(self, filename):
      mp3 = None
      try:
          mp3 = mutagen.mp3.MP3(filename)
      except mutagen.mp3.HeaderNotFoundError:
          pass
      except struct.error:
          pass

      return mp3
