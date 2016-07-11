import logging
import socket

from urllib import request, parse
from os import path

def get_content(url, headers={}, decoded=True):
    logging.debug('get_content: %s' % url)

    req = request.Request(url, headers=headers)

    for i in range(10):
        try:
            response = request.urlopen(req)
            break
        except socket.timeout:
            logging.debug('request attempt %s timeout' % str(i + 1))

    data = response.read()

    if decoded:
        data = data.decode()

    return data

def url_basename(url):
    return path.basename(parse.urlparse(url).path)

def unquote_twice(url):
    return parse.unquote_plus(parse.unquote_plus(url))