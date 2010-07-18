#Copyright (C) 2009 Erik Hetzner

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

import BaseHTTPServer, errno, logging, os, re, urllib, socket, sys, traceback
from simplejson import dumps

import config
import spydaap
import spydaap.metadata

md = spydaap.metadata.MetadataCache(
    spydaap.media_path,
    spydaap.parsers,
)


class DAAPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def address_string(self):
        host, port = self.client_address[:2]
        return host

    def h(self, data, **kwargs):
        self.send_response(kwargs.get('status', 200))
        self.send_header('Content-Type', kwargs.get('type', 'text/javascript'))
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Accept-Ranges', 'bytes')
        try:
            if type(data) == file:
                self.send_header("Content-Length", str(os.stat(data.name).st_size))
            else:
                self.send_header("Content-Length", len(data))                   
        except:
            pass

        self.end_headers()
        if getattr(self, 'isHEAD', None):
          return

        try:
            if (hasattr(data, 'next')):
                for d in data:
                    self.wfile.write(d)
            else:
                self.wfile.write(data)
        except socket.error, ex:
            if ex.errno in [errno.ECONNRESET]: pass
            else: raise
        if (hasattr(data, 'close')):
            data.close()

    URLS = {
        '/server-info$' : "server_info",
    #    '/list$' : 'db_list',
        '/db$' : 'db_info',
        '/db/(.*)$' : 'db_index',
        '/fetch/([a-f0-9]{32})$' : 'fetch',
    }

    _URLS = {}
    for url in URLS.keys():
      k = re.compile(url)
      _URLS[k] = URLS.get(url)

    URLS = _URLS

    def do_GET(self):
        parsed_path = urllib.unquote_plus(self.path)
        for k,v in self.URLS.iteritems():
          md = re.match(k, parsed_path)

          if not md:
            continue

          args = md.groups()
          func = getattr(self, "do_GET_" + v)
          ret = func(*args)

          if not ret:
            self.send_error(404)
            return

          self.h(ret if type(ret) == file else dumps(ret))
          return

        else:
            self.send_error(404)

    def do_HEAD(self):
        self.isHEAD = True
        self.do_GET()

    def do_GET_server_info(self):
        return ('serverinforesponse', 'alive')

    def do_GET_db_index(self, req):
        areq = tuple(req.split("/"))

        path = ()
        for x in range((len(areq)+1)/2):
          step = areq[x*2]
          path += (step,)

        if path not in md.INDEXES:
          print 'not in index', path
          return # 404

        plen = len(path)
        indexes = filter(
            lambda idx : len(idx) > plen and idx[:plen] == path,
            md.INDEXES
        )

        return ('data', 
            md.fget(areq),
            map(lambda x :x[plen], indexes),
            indexes,
        )

    def do_GET_db_info(self):
      return (
          "indexes",
          map(
            lambda idx : idx[0],
            filter(
              lambda idx : len(idx) == 1,
              md.INDEXES,
            ),
          ),
          md.INDEXES,
      )

    def do_GET_fetch(self, fhash):
      fname = "%s/media/%s" %(spydaap.cache_dir, fhash)

      if not os.access(fname, 0):
        return
      
      return open(fname, 'rb')
