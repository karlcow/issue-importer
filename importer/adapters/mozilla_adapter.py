#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
VALID_LABELS = ['serversniff', 'clientsniff']

def convert_issue_data(json_data):
    '''Take the json data from the bug repo and convert it
    into json data suitable for webcompat.

    Documentation of HTTP Mozilla Bugzilla API:
    http://bugzilla.org/docs/tip/html/api/Bugzilla/WebService/Server/REST.html
    http://bugzilla.org/docs/tip/html/api/Bugzilla/WebService/Bug.html
    '''
    webcompat_json = None
    # json_data is a list of bugs we only want the first one
    bug_data = json_data['bugs'][0]
    source = 'https://bugzilla.mozilla.org/show_bug.cgi?id=%s' % (bug_data['id'])
    os = bug_data['op_sys'].lower()
    # Let's gather some labels
    regex = re.compile(ur'\[(.*?)\]')
    whiteboard_labels = re.findall(regex, bug_data['whiteboard'])
    # We probably want to filter out labels that are only mozilla.
    moz_labels = [label for label in whiteboard_labels if label in VALID_LABELS]
    moz_labels.extend([u'firefox', os, u'imported'])
    webcompat_json = {
        'url': bug_data['url'],
        'title': bug_data['summary'],
        'os': os,
        'browser': u'Firefox',
        'source_human': source,
        'labels': moz_labels,
        'body': 'body is missing. Need to code it'
    }
    return webcompat_json