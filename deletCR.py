#!/usr/bin/python

import os
import sys
import glob
import argparse

def process_file(name, lend):
    with open(name, 'rb') as fl:
        data = fl.read()

    data = data.replace('\r\n', '\n').replace('\r', '\n')
    data = data.replace('\n', lend)
    with open(name, 'wb') as fl:
        fl.write(data)

def main():
    parser = argparse.ArgumentParser(description='Convert line-endings of one '
            'or more files.')
    parser.add_argument('-r', '--recursive', action='store_true',
            help='Process all files in a given directory recursively.')
    parser.add_argument('-d', '--dest', default='unix',
            choices=('unix', 'windows'), help='The destination line-ending '
            'type. Default is unix.')
    parser.add_argument('-e', '--is-expr', action='store_true',
            help='Arguments passed for the FILE parameter are treated as '
            'glob expressions.')
    parser.add_argument('-x', '--dont-issue', help='Do not issue missing files.',
            action='store_true')
    parser.add_argument('files', metavar='FILE', nargs='*',
            help='The files or directories to process.')
    args = parser.parse_args()

    # Determine the new line-ending.
    if args.dest == 'unix':
        lend = '\n'
    else:
        lend = '\r\n'

    # Process the files/direcories.
    if not args.is_expr:
        for name in args.files:
            if os.path.isfile(name):
                process_file(name, lend)
            elif os.path.isdir(name) and args.recursive:
                for dirpath, dirnames, files in os.walk(name):
                    for fn in files:
                        fn = os.path.join(dirpath, fn)
                        process_file(fn, fn)
            elif not args.dont_issue:
                parser.error("File '%s' does not exist." % name)
    else:
        if not args.recursive:
            for name in args.files:
                for fn in glob.iglob(name):
                    process_file(fn, lend)
        else:
            for name in args.files:
                for dirpath, dirnames, files in os.walk('.'):
                    for fn in glob.iglob(os.path.join(dirpath, name)):
                        process_file(fn, lend)

if __name__ == "__main__":
    main()

