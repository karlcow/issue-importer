#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''Main entry point to the importer module.'''

import argparse
import sys
from importer import validate_json, print_labels, create_issue, get_as_json, format_post_body, format_issue, fake_message
from termcolor import cprint

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('issue_file', nargs='?', default=sys.stdin,
                        help='JSON file representing a single issue.')
    parser.add_argument('-l', '--labels', action='store_true',
                        help='Print all labels used by issues.')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Don\'t validate labels against the issues repo.')
    parser.add_argument('-o', '--origin',
                        choices=['moz', 'ms', 'blink', 'apple'],
                        help='Adjust the import to the JSON issue format')
    publishgroup = parser.add_mutually_exclusive_group()
    publishgroup.add_argument('-t', '--test', action='store_true',
                        help='NO publishing on Github, just testing')
    publishgroup.add_argument('-g', '--github', action='store_true',
                        help='Publishing on Github. Irreversible.')
    args = parser.parse_args()
    # Printing the list of existing labels on Github
    if args.labels:
        print_labels()
        sys.exit(0)
    elif args.origin:
        # Let's get the data
        json_data = get_as_json(args.issue_file)
        # create the data with the right format
        webcompat_issue = format_issue(json_data, args.origin)
    else:
        cprint('Missing --labels or --origin', 'white', 'on_red')
        parser.print_help()
        sys.exit(0)
    # Validation
    if validate_json(webcompat_issue, args.force):
        if args.github:
            # Mode with consequences
            create_issue(webcompat_issue)
            cprint('Creating the issue on Github', 'green')
        elif args.test:
            # Mode without consequences
            cprint('Test Mode Run. Nothing is sent to github', 'yellow')
            print fake_message(webcompat_issue)
        else:
            cprint('Missing --test or --github', 'white', 'on_red')
            parser.print_help()
            sys.exit(0)
    else:
        cprint('Invalid JSON data for the issue', 'red')
        sys.exit(0)

