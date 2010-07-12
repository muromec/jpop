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

import os, re

class Parser:
    def handle(self, md, data=None):
      if data == None:
        data = {}

      for k in md.tags.keys():
        if not k in self.MAP:
          continue

        key, typ = self.MAP[k]

        val = getattr(self, "typ_%s" % typ)(md.tags[k])

        data[key] = val

      return data

    def typ_s(self, data):
      if type(data) == str:
        return data.decode('utf8')
      else:
        return unicode(data)

    def typ_i(self, data):
      try:
        return int(data)
      except:
        return 0

    def parse(self, filename):
      d = {}
      md = self.parser_get(filename)

      if md and md.tags != None:
        self.handle(md, d)

      self.add_file_info(filename, d)
      self.set_itemname_if_unset(os.path.basename(filename), d)
      return d


    def add_file_info(self, filename, data):
      statinfo = os.stat(filename)
      data.update(
        {
          'size': os.path.getsize(filename),
          'mtime': statinfo.st_ctime,
        }
      )
        
    
    def set_itemname_if_unset(self, name, data):
      data['name'] = data.get('name', name)
