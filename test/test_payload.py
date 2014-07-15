#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''Test that the POST payload is sucessfully created.'''

import requests
import unittest

from importer import format_post_body

json_data = {
  u"url": u"www.💩.com",
  u"title": u"Upgrade browser message",
  u"browser": u"Firefox 30",
  u"os": u"Windows 7",
  u"body": u"The site asks me to upgrade",
  u"labels": [u"contactready", u"invalid"],
  u"comments": [u"1", u"2", u"", u"3", None]
}

class TestPayload(unittest.TestCase):
    def test_payload(self):
        payload = format_post_body(json_data)
        self.assertIsNotNone(payload.get('body'))
        self.assertIsInstance(payload.get('body'), unicode)
        self.assertIsNotNone(payload.get('title'))
        self.assertIsInstance(payload.get('title'), unicode)
        self.assertIsNotNone(payload.get('labels'))
        self.assertIsInstance(payload.get('labels'), list)

if __name__ == '__main__':
    unittest.main()
