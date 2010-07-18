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
from hashlib import md5
from simplejson import dump, load

import spydaap

class MetadataCache(object):
  INDEXES = (
    ("album",),

    ("artist", "album",),
    ("artist",),

    ("genre","artist", "album"),
    ("genre","artist",),
    ("genre","album",),
    ("genre",),
  )

  def __init__(self, cache_dir, parsers):
    self.parsers = parsers
    self.dir = os.path.abspath(cache_dir)

    self.cached, self.parsed, self.skipped = 0,0,0

    self.data = {}

  def fget(self, key):

    if key in self.data:
      return self.data.get(key)

    fname = md5(str(key)).hexdigest()

    f = None
    try:
      f = open("%s/%s.js" % (spydaap.cache_dir,fname), 'rb')
      return load(f)
    except:
      return
    finally:
      if f:
        f.close()

  def fset(self, key, data):
    self.data[key] = data

    if len(self.data) > 10:
      self.flush()

  def flush(self):

    for key, data in self.data.iteritems():
      self.writeindex(key, data)

    self.data.clear()

  def writeindex(self, key, data):
    fname = md5(str(key)).hexdigest()

    f = open("%s/%s.js" % (spydaap.cache_dir,fname), 'wb')
    f.truncate()
    dump(data, f)
    f.close()

  def check_all(self,):

    media = spydaap.cache_dir+"/media/"
    map(self.check, os.listdir(media))

  def check(self, fname):
    fpath = spydaap.cache_dir+"/media/" + fname

    try:
      current = int(os.stat(fpath).st_mtime)
    except OSError:
      self.invalidate(fname)
      return

    saved = int(os.lstat(fpath).st_mtime)

    if saved < current:
      self.invalidate(fname)

  def invalidate(self, fhash):
    print 'inval', fhash
    linkfname = "%s/indexlinks/%s.js" % (
          spydaap.cache_dir, fhash
    )
    cachename = "%s/media/%s" % (
        spydaap.cache_dir, fhash
    )
    f = open(linkfname, 'rb')
    data = load(f)
    f.close()

    for idx in data:
      idx_data = self.fget(idx)

      for el in idx_data:
        if el['fhash'] == fhash:
          print el
          idx_data.remove(el)
          self.fset(idx, idx_data)
          break

    try:
      os.unlink(linkfname)
    except OSError:
      pass

    try:
      os.unlink(cachename)
    except OSError:
      pass

  def identify(self, ffn):
    fhash = md5(ffn).hexdigest()
    sname =  "%s/media/%s" % (spydaap.cache_dir, fhash)

    current = int(os.stat(ffn).st_mtime)

    if os.access(sname,0):
      saved = int(os.lstat(sname).st_mtime)

      if saved >= current:
        return

    for p in self.parsers:
      if not p.understands(ffn):
        continue
          
      m = p.parse(ffn)


      if not os.access(sname, 0):
        os.symlink(ffn, sname)

      indexes = map(
          lambda idx:self.create_index(idx, m),
          self.INDEXES,
      )

      links = []
      for idx in indexes:
        if not idx:
          continue

        links.append( str(idx) )


      linkfname = "%s/indexlinks/%s.js" % (
          spydaap.cache_dir, fhash
      )
      f = open(linkfname, 'wb')
      f.truncate()
      dump(links, f)
      f.close()


      break

  def create_index(self, idx, song):
    for field in idx:
      if field not in song:
        return

    fname = reduce(
        lambda a, idxv : a+(idxv, song.get(idxv).encode('utf8')),
        idx,
        (),
    )

    # write index
    old = self.fget(fname[:-1]) or []
    if fname[-1] not in old:
      old.append( fname[-1] )
      self.fset(fname[:-1], old)

    # write song info
    old = self.fget(fname) or []
    old.append(song)
    self.fset(fname, old)

    return fname

  def build(self, link=False):

    for path, dirs, files in os.walk(self.dir):
      for d in dirs:
        if os.path.islink(os.path.join(path, d)):
            self.build(os.path.join(path,d), True)

      map(
          lambda fn:self.identify(os.path.join(path, fn)),
          files
      )
