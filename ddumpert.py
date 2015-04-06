#! /usr/bin/python3
import urllib.request
import base64
import ast
import sys
import os
import re

DUMPERT_RE = re.compile(b'data-files="(.+?)"')
USERAGENT = {'User-Agent': 'Mozilla/5.0'}

class MyUrlOpener(urllib.request.FancyURLopener):
    version = USERAGENT['User-Agent']
    
def geturl(url):
    request = urllib.request.Request(url, None, USERAGENT)
    return urllib.request.urlopen(request).read()

def getmovieurl(html):
    match = re.search(DUMPERT_RE, html)
    if match:
        formats = ast.literal_eval(
            base64.b64decode(match.group(1)).decode('utf-8'))
        try:    return formats['720p'].replace('\\', '')
        except: return formats['flv'].replace('\\', '')
    else:
        return None

def reporthook(numblocks, blocksize, filesize, name=None):
    try:    percent = min((numblocks*blocksize*100)//filesize, 100)
    except: percent = 100
    if numblocks != 0: sys.stdout.write("\r")
    sys.stdout.write("{0:<66}{1:3d}%".format(name, percent))

if len(sys.argv) != 2:
    print("usage: ddumpert.py url")
    exit(1)

movieurl = getmovieurl(geturl(sys.argv[1]))
if movieurl:
    filename = os.path.basename(movieurl)
    print(("Downloading '" + movieurl + "'.."))
    urllib.request._urlopener = MyUrlOpener()
    if sys.stdout.isatty():
        urllib.request.urlretrieve(movieurl, filename,
                           lambda nb, bs, fs, name=filename: \
                           reporthook(nb, bs, fs, filename))
        sys.stdout.write("\n")
    else:
        urllib.request.urlretrieve(movieurl, filename)
else:
    print("no video data found in page")
