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

  ret = url_get(base)
  deep = []
  foundall = []

  for link in links(ret):
    #print link

    name = link.lower()

    first = True
    match = 0
    for w in words:
      if w in name:
        match += 1
        
        if first:
          deep.append(link)

      first = False

    if match == len(words):
      foundall.append(link)


  if foundall:
    print 'haha, found all', foundall

    if level == 0:
      _ret = map(
          lambda x : search([], base+x, level+1),
          foundall
      )
    else:
      _ret = [
          map(
            lambda x : (x, base+x),
            foundall
          )
      ]

  elif deep:
    print 'go deep'
    _ret = map(
        lambda x : search(words[1:], base+x, level+1),
        deep
    )
    print 'deep', _ret
  else:
    return []

  ret = [] 
  for chunk in _ret:
    ret.extend(chunk)

  return ret

def fetch(bulk):
  print 'fetch', bulk


if __name__ == '__main__':
  import sys

  request = str.join(" ", sys.argv[1:])
  words = map(str.lower, request.split())

  got = search(words)

  for name, url in got:
    print 'URL',name, url
