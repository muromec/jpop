
import os
from simplejson import dump, load

import spydaap

class DB(object):
  def __init__(self, name):
    self.name = name
    self.data = {}
    self.fk = {}
    self.data['__fk'] = self.fk

  def add(self, media):
    key = media[self.name]
    fname = media['fhash']

    self.drop(fname)

    if key not in self.data:
      self.data[key] = {}

    self.data[key][fname] = media

    self.fk[fname] = key

  def drop(self, fname):
    if fname not in self.fk:
      return

    old_key = self.fk.get(fname)
    assert old_key in self.data, 'yrrr db wrong'

    self.data[old_key].pop(fname, None)
    self.fk.pop(fname, None)

  def get(self, key):
    return self.data.get(key)

  def keys(self,):
    return self.data.keys()

  def flush(self,):
    fname = "%s/db_%s.js" %(spydaap.cache_dir, self.name)
    self.data['__fk'] = self.fk
    f = open(fname, 'wb')
    f.truncate()
    dump(self.data, f)
    f.close()

  def load(self):
    fname = "%s/db_%s.js" %(spydaap.cache_dir, self.name)
    try:
      f = open(fname, 'rb')
      self.data = load(f)
      self.fk = self.data['__fk']
      f.close()
    except:
      pass

  def clean(self):
    for fname in self.fk.keys():
      if fname not in Manager.ALL:
        self.fk.pop(fname)

    for tag in self.data:
      for fname in self.data.get(tag).keys():
        if fname not in Manager.ALL:
          self.data.get(tag).pop(fname)


class Manager(object):
  NAMES = [
      'album',
      'genre',
  ]
  DB = {}
  ALL = {}
  @classmethod
  def process(cls, media):
    fhash = media['fhash']
    cls.ALL[fhash] = media['mtime'], media.pop('file')

    for name in cls.NAMES:
      if name not in media:
        continue

      cls.DB[name].add(media)

  @classmethod
  def create_db(cls):
    for name in cls.NAMES:
      db = DB(name)
      db.load()
      cls.DB[name] = db
      globals()[name.upper()] = db

    try:
      f = open(spydaap.cache_dir+"/all.js", 'rb')
      cls.ALL = load(f)
      f.close()
    except:
      pass

  @classmethod
  def flush(cls):
    for db in cls.DB.values():
      db.flush()

    f = open(spydaap.cache_dir+"/all.js", 'wb')
    f.truncate()
    dump(cls.ALL, f)
    f.close()

  @classmethod
  def remove_missing(cls):
    for mtime, fname in cls.ALL.values():
      if os.access(fname, 0):
        continue

      cls.ALL.pop(fname, None)

      for db in cls.DB.values():
        db.drop(fname)

    for db in cls.DB.values():
      db.clean()



Manager.create_db()
Manager.remove_missing()

DB_REGEX = str.join("|", Manager.NAMES)
