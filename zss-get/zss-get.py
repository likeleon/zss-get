import getopt
import sys

from util import log

__version__ = '0.1'

def main(**kwargs):
    def version():
        log.i('version %s, zangsisi downloader.' % __version__)

    help = 'Usage: %s [OPTION]... \n\n' % 'zss-get'
    help += '''Startup options:
    -V | --version              Print version and exit.
    -h | --help                 Print help and exit.
    \n'''
    help += '''Dry-run options: (no actual downloading)
    -i | --info                 Print extracted information.
    \n'''

    short_opts = 'Vhi'
    opts = ['version', 'help', 'info']

    sys.argv[1:] = ['-i']
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, opts)
    except getopt.GetoptError as err:
        log.e(err)
        log.e("try 'zss-get --help' for more options")
        sys.exit(2)

    info_only = False
    for o, a in opts:
        if o in ('-V', '--version'):
            version()
            sys.exit()
        elif o in ('-h', '--help'):
            version()
            print(help)
            sys.exit()
        elif o in ('-i', '--info'):
            info_only = True
        else:
            log.e("Try 'zss-get --help' for more options")
            sys.exit(2)

if __name__ == '__main__':
    main()