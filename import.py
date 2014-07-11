#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''Main entry point to the importer module.'''

import argparse
import sys
from importer import validate_json, print_labels, create_issue, get_as_json, format_issue
from termcolor import cprint

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('issue_file', nargs='?', default=sys.stdin,
                        help='JSON file representing a single issue.')
    parser.add_argument('-l', '--labels', action='store_true',
                        help='Print all labels used by issues.')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Don\'t validate labels against the issues repo.')
    parser.add_argument('-o', '--origin', action='store_true',
                        choices=['moz', 'ms', 'blink', 'apple'],
                        help='Adjust the import to the JSON issue format')
    parser.add_argument('-d', '--dry-run', action='store_true',
                        help='No modifications, just testing')
    args = parser.parse_args()
    # Printing the list of existing labels on Github
    if args.labels:
        print_labels()
        sys.exit(0)
    # Let's get the data
    json_data = get_as_json(args.issue_file)
    # Mode without consequences
    if args.dry_run:
        cprint('Test Mode Run. Nothing is sent to github', 'yellow')
        webcompat_issue = format_issue(json_data, args.origin)
    # Mode with consequences
    else:
        # Processing an issue only if it's valid
        if validate_json(json_data, args.force):
            create_issue(json_data)
            cprint('Creating the issue on Github', 'green')
        else:
            cprint('Invalid JSON data for the issue', 'red')
            sys.exit(0)

