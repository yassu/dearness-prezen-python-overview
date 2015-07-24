#!/usr/bin/env python
"""
A script for make japanese slides by using markdown
"""

from tempfile import NamedTemporaryFile
from os import system, remove
from sys import exit
from optparse import OptionParser
from os.path import isfile


def gen_unicode_tex_filename():
    fp = NamedTemporaryFile(suffix='.tex', delete=False)
    fp.write((
        r'\usepackage{luatexja}'
        r'\hypersetup{unicode=true}'
    ).encode('utf-8'))
    fp.close()
    return fp.name


def get_filenames(argv):
    in_filename = argv[0]
    if len(argv) >= 2:
        out_filename = argv[1]
    else:
        out_filename = 'out.pdf'
    return in_filename, out_filename


def get_command(in_filename, out_filename, unicode_tex_filename, opts):
    return (
        'pandoc {input} -o {output} '
        '--latex-engine=lualatex '
        '-t beamer -H {unicode} '
        '-V theme:{theme} -V colortheme:{colortheme} '
        '-V fontsize:{fontsize}pt'.format(
            input=in_filename, output=out_filename,
            unicode=unicode_tex_filename,
            theme=opts.theme, colortheme=opts.colortheme,
            fontsize=opts.fontsize))


def get_opt_parser():
    usage = 'slideja [option] input_filename [output_filename]'
    parser = OptionParser(usage)

    parser.add_option(
        '-t', '--theme',
        action='store',
        dest='theme',
        default='Madrid',
        help='select theme'
    )
    parser.add_option(
        '-c', '--colortheme',
        action='store',
        dest='colortheme',
        default='seahorse',
        help='select colortheme'
    )
    parser.add_option(
        '-f', '--fontsize',
        action='store',
        type='int',
        dest='fontsize',
        default=20,
        help='select fontsize'
    )
    return parser

def main():
    parser = get_opt_parser()
    (options, argv) = parser.parse_args()
    if not argv:
        print('Please enter input_filename.')
        exit()
    unicode_tex_filename = gen_unicode_tex_filename()
    in_filename, out_filename = get_filenames(argv)

    try:
        if not isfile(in_filename):
            print('file "{}" is not found.'.format(in_filename))
            exit()

        command = get_command(in_filename, out_filename,
                              unicode_tex_filename, options)
        print(command)
        system(command)
    finally:
        remove(unicode_tex_filename)

if __name__ == '__main__':
    main()
