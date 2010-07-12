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

import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import md5

import os

class MetadataCache(object):
    def __init__(self, cache_dir, parsers):
        self.parsers = parsers
        self.dir = cache_dir

    def build(self, dir, link=False):
        for path, dirs, files in os.walk(dir):
            for d in dirs:
                if os.path.islink(os.path.join(path, d)):
                    self.build(os.path.join(path,d), True)
            for fn in files:
                ffn = os.path.join(path, fn)
                digest = md5.md5(ffn).hexdigest()

                # TODO: check if newer
                # os.stat(ffn).st_mtime
                print ffn

                for p in self.parsers:
                  if not p.understands(ffn):                                   continue

                  m = p.parse(ffn)
