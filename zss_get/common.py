import logging
import socket
import os
import time
import sys

from urllib import request, parse
import shutil

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
    return os.path.basename(parse.urlparse(url).path)

def unquote_twice(url):
    return parse.unquote_plus(parse.unquote_plus(url))

def quote_url(url):
    parts = list(parse.urlsplit(url))
    parts[2] = parse.quote(parts[2])
    return parse.urlunsplit(parts)

class SimpleProgressBar:
    term_size = min(shutil.get_terminal_size().columns, 80)

    def __init__(self, total = 1):
        self.displayed = False
        self.total = total
        self.current = 0
        self.bytes_received = 0
        self.speed = ''
        self.last_updated = time.time()

        total_len = len(str(total))
        self.bar_size = self.term_size - 37 - 2 * total_len
        self.bar = '{:>4}%% ({:>5}MB) ├{:-<%s}┤[{:>%s}/{:>%s}] {}' % (
            self.bar_size, total_len, total_len)

    def update(self):
        self.displayed = True
        bar_size = self.bar_size
        percent = round(self.current * 100 / self.total, 1)
        if percent >= 100:
            percent = 100
        dots = bar_size * int(percent) // 100
        bar = self.bar.format(percent, round(self.bytes_received / 1048576, 1), '+' * dots, self.current, self.total, self.speed)
        sys.stdout.write('\r' + bar)
        sys.stdout.flush()

    def update_received(self, n):
        self.bytes_received += n
        time_diff = time.time() - self.last_updated
        bytes_ps = n / time_diff if time_diff else 0
        if bytes_ps >= 1024 ** 3:
            self.speed = '{:4.0f} GB/s'.format(bytes_ps / 1024 ** 3)
        elif bytes_ps >= 1024 ** 2:
            self.speed = '{:4.0f} MB/s'.format(bytes_ps / 1024 ** 2)
        elif bytes_ps >= 1024:
            self.speed = '{:4.0f} kB/s'.format(bytes_ps / 1024)
        else:
            self.speed = '{:4.0f}  B/s'.format(bytes_ps)
        self.last_updated = time.time()
        self.update()

    def update_current(self, n):
        self.current = n

    def done(self):
        if self.displayed:
            print()
            self.displayed = False