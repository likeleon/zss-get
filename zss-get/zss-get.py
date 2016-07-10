import getopt
import sys
import logging
import socket

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

def list_books():
    soup = BeautifulSoup(get_content(SITE), 'html.parser')
    links = soup.find(id='recent-post').find_all('a', class_='tx-link')
    print({ link.get('href'): link.get_text() for link in links })

def main(**kwargs):
    def version():
        log.i('version %s, zangsisi downloader.' % __version__)

    help = 'Usage: %s [OPTION]... \n\n' % 'zss-get'
    help += '''Startup options:
    -V | --version              Print version and exit.
    -h | --help                 Print help and exit.
    \n'''
    help += '''Dry-run options: (no actual downloading)
    -l | --list                 Display all available books.
    \n'''

    short_opts = 'Vhl'
    opts = ['version', 'help', 'list']

    sys.argv[1:] = ['-l']
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, opts)
    except getopt.GetoptError as err:
        log.e(err)
        log.e("try 'zss-get --help' for more options")
        sys.exit(2)

    for o, a in opts:
        if o in ('-V', '--version'):
            version()
            sys.exit()
        elif o in ('-h', '--help'):
            version()
            print(help)
            sys.exit()
        elif o in ('-l', '--list'):
            list_books()
            sys.exit()
        else:
            log.e("Try 'zss-get --help' for more options")
            sys.exit(2)

if __name__ == '__main__':
    main()