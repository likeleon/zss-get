import sys
import logging
import socket
import argparse

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

def all_comics():
    soup = BeautifulSoup(get_content(SITE), 'html.parser')
    for a in soup.find(id='recent-post').find_all('a', class_='tx-link'):
        yield Comic(a.get_text(), a.get('href'), True)
    for a in soup.find(id='manga-list').find_all('a', class_='lists')[3:]:
        yield Comic(a.get_text(), a.get('href'), False)

def print_comic(comic):
    print("- title:     %s" % comic.title)
    print("  url:       %s" % comic.url)
    print("  concluded: %s" % comic.concluded)

def get_books(comic):
    soup = BeautifulSoup(get_content(comic.url), 'html.parser')
    for a in soup.find(id='recent-post').find_all('a', class_='tx-link'):
        yield a.get_text(), a.get('href')

def download(comic):
    for book, link in get_books(comic):
        print("{}: {}".format(book, link))

def get_parser():
    parser = argparse.ArgumentParser(description='zangsisi downloader')
    parser.add_argument('keyword', metavar='KEYWORD', type=str, nargs='*', help='keyword for searching the book by its title')
    parser.add_argument('-l', '--list', help='display all available comics', action='store_true')
    parser.add_argument('-v', '--version', help='displays the current version of zss-get', action='store_true')
    return parser

def main(**kwargs):
    sys.argv[1:] = ['은혼']

    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    if args['list']:
        for c in all_comics():
            print_comic(c)
        return

    if not args['keyword']:
        parser.print_help()
        return

    comics = [c for c in all_comics() if all(k in c.title for k in args['keyword'])]
    if len(comics) > 1:
        print("Ambiguous keywords: '{}'. Matched comics: ".format(", ".join(keywords)))
        for c in comics:
            print_comic(c)
        return

    download(comics[0])

if __name__ == '__main__':
    main()