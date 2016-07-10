import sys
import logging
import socket
import argparse

from util import log
from urllib import request
from bs4 import BeautifulSoup

__version__ = '0.1'

SITE = "http://zangsisi.net/"

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

class Comic():
    def __init__(self, title, url, concluded):
        self.title = title
        self.url = url
        self.concluded = concluded

def get_comics():
    soup = BeautifulSoup(get_content(SITE), 'html.parser')
    for a in soup.find(id='recent-post').find_all('a', class_='tx-link'):
        yield Comic(a.get_text(), a.get('href'), True)
    for a in soup.find(id='manga-list').find_all('a', class_='lists')[3:]:
        yield Comic(a.get_text(), a.get('href'), False)

def list_comics():
    for comic in get_comics():
        print("     - title:     %s" % comic.title)
        print("       url:       %s" % comic.url)
        print("       concluded: %s" % comic.concluded)

def get_parser():
    parser = argparse.ArgumentParser(description='zangsisi downloader')
    parser.add_argument('book', metavar='BOOK', type=str, nargs='*', help='title of the book to download')
    parser.add_argument('-l', '--list', help='display all available comics.', action='store_true')
    parser.add_argument('-v', '--version', help='displays the current version of zss-get', action='store_true')
    return parser

def main(**kwargs):
    #sys.argv[1:] = ['-l']

    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    if args['list']:
        list_comics()
        return

    if not args['book']:
        parser.print_help()
        return

if __name__ == '__main__':
    main()