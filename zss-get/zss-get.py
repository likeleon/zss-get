import sys
import argparse
import os
import os.path
import re

from common import *
from urllib import request
from zipfile import ZipFile
from bs4 import BeautifulSoup

__version__ = '1.1'

SITE = "http://zangsisi.net/"

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

def download(comic, args):
    print('Navigating %s ...' % comic.title)

    for title, link in get_books(comic, args['volume']):
        output_filename = '%s.zip' % title
        output_filepath = os.path.join(args['output_dir'], output_filename)
        download_book(title, link, output_filepath, args['force'])

def get_books(comic, volume):
    soup = BeautifulSoup(get_content(comic.url), 'html.parser')
    for a in soup.find(id='recent-post').find_all('a', class_='tx-link'):
        title = a.get_text()
        if volume and guess_volume(title) != volume:
            continue
        yield title, a.get('href')

def guess_volume(title):
    m = re.match(r'[^\d]*(\d+)\s*권', title)
    if not m:
        return None
    return int(m.group(1))

def download_book(title, link, filepath, force):
    if os.path.exists(filepath):
        if not force:
            print('Skipping %s: file already exists' % (os.path.basename(filepath)))
            return
        else:
            print('Overwriting %s' % (os.path.basename(filepath)))
    else:
        print('Downloading %s' % (os.path.basename(filepath)))
        if not os.path.exists(os.path.dirname(filepath)):
            os.mkdir(os.path.dirname(filepath))

    urls = list(get_image_urls(link))
    if not urls:
        print('Skipping %s: nothing to download' % (os.path.basename(filepath)))
        return

    with ZipFile(filepath, 'w') as zip:
        save_images(urls, zip)

def save_images(urls, zip):
    bar = SimpleProgressBar(len(urls))
    bar.update()

    for i, img_url in enumerate(urls):
        with request.urlopen(quote_url(img_url)) as response:
            arcname = url_basename(unquote_twice(img_url))
            data = response.read()
            zip.writestr(arcname, data)
            bar.update_current(i + 1)
            bar.update_received(len(data))
    
    bar.done()

def get_image_urls(link):
    soup = BeautifulSoup(get_content(link), 'html.parser')
    for img in soup.find('span', class_='contents').find_all('img'):
        yield img.get('src')

def get_parser():
    parser = argparse.ArgumentParser(description='zangsisi downloader')
    parser.add_argument('keyword', metavar='KEYWORD', type=str, nargs='+', help='keyword for searching the book by its title')
    parser.add_argument('-l', '--list', help='Display all available comics', action='store_true')
    parser.add_argument('--volume', help='Set volume number to download', type=int)
    parser.add_argument('-o', '--output-dir', help='Set output directory', type=str, default='.')
    parser.add_argument('-f', '--force', help='Force overwriting existed files', default=False, action='store_true')
    parser.add_argument('-v', '--version', help='Displays the current version of zss-get', action='store_true')
    return parser

def main(**kwargs):
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    if args['list']:
        for c in all_comics():
            print_comic(c)
        return

    comics = [c for c in all_comics() if all(k in c.title for k in args['keyword'])]
    if len(comics) > 1:
        print("Ambiguous keywords: '%s'. Matched comics: " % (", ".join(keywords)))
        for c in comics:
            print_comic(c)
        return

    download(comics[0], args)

if __name__ == '__main__':
    main()