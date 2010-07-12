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

import os

import db

class MetadataCache(object):
  def __init__(self, cache_dir, parsers):
    self.parsers = parsers
    self.dir = cache_dir

    self.cached, self.parsed, self.skipped = 0,0,0

  def build(self, dir, link=False):

    for path, dirs, files in os.walk(dir):
      for d in dirs:
        if os.path.islink(os.path.join(path, d)):
            self.build(os.path.join(path,d), True)

      for fn in files:
        ffn = os.path.join(path, fn)

        # TODO: check if newer
        # os.stat(ffn).st_mtime
        if ffn in db.Manager.ALL:
          current = int(os.stat(ffn).st_mtime)
          saved = db.Manager.ALL.get(ffn)

          if saved == current:
            self.cached+=1
            continue

        for p in self.parsers:
          if not p.understands(ffn):
            continue

          m = p.parse(ffn)
          self.parsed+=1

          db.Manager.process(m)
          break

        else:
          self.skipped+=1

    db.Manager.flush()
