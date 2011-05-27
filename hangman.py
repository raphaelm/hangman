#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       hangman.py
#       
#       Copyright 2011 Raphael Michel <webmaster@raphaelmichel.de>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import BaseHTTPServer
import json
import webbrowser
import thread
import time
import magic
import os
import random
import urllib

typecache = {}
mime = magic.open(magic.MAGIC_MIME)
mime.load()

word = ""
triedchars = []
failedchars = []
progress = []
rand = ''
state = 'noword'

def uniquify(seq, idfun=None):  
	# order preserving 
	if idfun is None: 
		def idfun(x): return x 
	seen = {} 
	result = [] 
	for item in seq: 
		marker = idfun(item) 
		# in old Python versions: 
		# if seen.has_key(marker) 
		# but in new ones: 
		if marker in seen: continue 
		seen[marker] = 1 
		result.append(item) 
	return result

class HangmanHTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def log_request(self, code=False, size=False):
		pass
		
	def do_GET(self):
		global mime, typecache, word, triedchars, progress, failedchars, rand, state
		if self.path == "/" or self.path == "/display":
			self.path = "/display.html"
		elif self.path == "/device":
			self.path = "/device.html"
			
		if self.path.startswith('/api/setword/'):
			word = urllib.unquote(self.path[13:].strip()).upper().replace("Ä", "a").replace("Ö", "o").replace("Ü", "u").replace("ß", "s").replace("ä", "a").replace("ö", "o").replace("ü", "u")
			triedchars = []
			failedchars = []
			progress = ["_"]*len(word)
			i = 0
			warning = False
			for c in word:
				if c == " ":
					progress[i] = "·"
				if c not in [" ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "o", "u", "s"]:
					warning = True
				i += 1
			rand = random.random()
			state = 'playing'
			self.send_response(200)
			self.end_headers()
			self.wfile.write(json.dumps({
				'warning' : warning
			}))
		elif self.path == '/api/getstate':
			self.send_response(200)
			self.send_header("Content-type", "text/plain")
			self.end_headers()
			self.wfile.write(json.dumps({
				'tried': triedchars,
				'failed': failedchars,
				'fails': len(failedchars),
				'progress': progress,
				'rand' : rand,
				'state' : state
			}))
		elif self.path.startswith('/api/char/') and state == 'playing':
			char = self.path[10:].strip()[0]
			if char in triedchars:
				pass
			else:
				triedchars.append(char)
				if char in word:
					i = 0
					for c in word:
						if c == char:
							progress[i] = char
						i += 1
				else:
					failedchars.append(char)
			if len(failedchars) >= 9:
				state = 'lost'
			elif "_" not in progress:
				state = 'won'
			self.send_response(200)
			self.end_headers()
		else:
			filename = 'static/'+self.path[1:].replace("..", "_")
			if os.path.exists(filename):  
				if filename not in typecache:
					if filename[-4:] == ".css":
						t = 'text/css; charset=utf-8'
					elif filename[-3:] == ".js":
						t = 'text/javascript; charset=utf-8'
					elif filename[-5:] == ".html":
						t = 'text/html; charset=utf-8'
					elif filename[-4:] == ".png":
						t = 'image/png'
					else:
						t = mime.file(filename)
					typecache[filename] = t
				self.send_response(200)
				self.send_header("Content-type", typecache[filename])
				self.end_headers()
				f = open(filename)
				self.wfile.write(f.read())
				f.close()
			else:
				 self.send_error(404)
			
def openpage(stuff):
	time.sleep(0.5)
	webbrowser.open('http://localhost:54733/display')
			
def main():	
	server_address = ('', 54733)
	httpd = BaseHTTPServer.HTTPServer(server_address, HangmanHTTPHandler)
	thread.start_new_thread(openpage, (None,))
	httpd.serve_forever()
	return 0

if __name__ == '__main__':
	main()

