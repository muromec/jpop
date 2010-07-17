import urllib
from simplejson import load

BASE = 'http://192.168.1.13:3663/db'

def get(url):
  print BASE+url
  f = urllib.urlopen(BASE+url)

  try:
    return load(f)
  finally:
    f.close()

class Index(object):
  def __init__(self, req = [], name = '', level=0):
    self.req = req
    self.level = level
    self.name = name

  def load(self,):
    url = ''
    for key,val in self.req:
      url += "/%s/%s" %(key,val)

    if self.name:
      url += "/%s" % self.name

    _x, self.data, self.next = get(url)

  def index(self, name,):
    return Index(name=name, level=self.level+1)

  def sub(self, value):
    req = self.req + [ (self.name, value) ]
    return Sub( req, self.level + 1, self.next)

  def pl(self, value):
    req = self.req + [ (self.name, value) ]
    return Index( req=req, level=self.level + 1)

  def select(self, label):
    if self.level % 2:
      func = self.sub
    else:
      func = self.index

    return func(label)




class Sub(object):
  def __init__(self, req, level, next):
    self.req = req
    self.level = level
    self.next = next

  def load(self):
    self.data = map(
        lambda x : x[self.level / 2],
        filter(lambda x : len(x) > (self.level / 2), self.next)
    )

  def select(self, name):
    return Index(self.req, name, self.level+1)

root = Index()
root.load()
print root.data

artist = root.select("artist")
artist.load()
print artist.data

snow = artist.select(artist.data[0])
snow.load()
print snow.data

album = snow.select(snow.data[0])
album.load()
print album.data

pl = album.pl(album.data[0])
pl.load()
print pl.data
