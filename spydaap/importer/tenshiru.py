import urllib
import re
import os

BASE_URL = 'http://tenshi.ru/anime-ost/'

def url_get(addr):
  print 'get', addr
  cache = addr.replace("/", "__")

  if os.access(cache, 0):
    f = open(cache, 'rb')
    cf = None
  else:
    f = urllib.urlopen(addr)
    cf = open(cache, 'wb')

  ret = ""
  for line in f:
    ret += line
    if cf:
      cf.write(line)

  f.close()
  if cf:
    cf.close()

  return ret

def links(html):
  return filter(
      lambda x : x[0] != '?',
      re.findall(r'href="(.*)"', html)
  )

def list_albums(links):
  return []

def search_albums(links, words):
  return ['1']

def search(words, base=BASE_URL, level=0):
  print 'search', words, base

  html = url_get(base)
  ret = []

  for link in links(html):
    #print link

    name = link.lower()
    name = re.sub(r'(\.|_)', ' ', name)[:-1]

    first = True
    notfound = []
    match = 0
    for w in words:
      if w not in name:
        notfound.append(w)

    if words:
      if notfound == words:
        continue

    if words and level == 0:
      if words[0] not in notfound:
        ret.extend(search(notfound, base+link, level+1))
    else:
      ret.append( (name, base+link) )

  return ret

def fetch(bulk):
  print 'fetch', bulk


if __name__ == '__main__':
  import sys

  request = str.join(" ", sys.argv[1:])
  words = map(str.lower, request.split())

  got = search(words)

  if not got:
    print 'nothing'

  for name, url in got:
    print 'URL',name, url
