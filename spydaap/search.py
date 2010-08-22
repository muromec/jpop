import spydaap

def process(req):
  words = map(str.lower, req.split())

  ret = []
  for mod in spydaap.importers:
    ret.extend( mod.search(words) )

  return ret

