import os
from hashlib import md5
from simplejson import dump, load

import spydaap

def hashkey(tkey):
  if not isinstance(tkey, basestring):
    tkey = tuple(map(
      lambda x : x.encode('utf8') if isinstance(x, unicode) else x,
      tkey)
    )

  return md5(str(tkey)).hexdigest() 

class Index:
  TEMPLATE = spydaap.cache_dir + "/%s.js"

  def __init__(self, fname, mode='rb'):
    self.f = open(self.TEMPLATE % fname, mode)

class IndexLinks(Index):
  TEMPLATE =  spydaap.cache_dir + "/indexlinks/%s.js"


class DB(object):
  data = {}

  dir = os.path.abspath(spydaap.cache_dir)

  @classmethod
  def fget(cls, key):

    fname = hashkey(key)

    if fname in cls.data:
      return cls.data.get(fname)

    f = None
    try:
      f = open("%s/%s.js" % (spydaap.cache_dir,fname), 'rb')
      return load(f)
    except:
      return
    finally:
      if f:
        f.close()

  @classmethod
  def fset(cls, key, data):
    fname = hashkey(key)
    cls.data[fname] = data

    if len(cls.data) > 10:
      cls.flush()

  @classmethod
  def flush(cls):

    for key, data in cls.data.iteritems():
      cls.writeindex(key, data)

    cls.data.clear()

  @classmethod
  def writeindex(cls, fname, data):

    f = Index(fname, 'wb').f
    f.truncate()
    dump(data, f)
    f.close()

fget = DB.fget
fset = DB.fset
flush = DB.flush
