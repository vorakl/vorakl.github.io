#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)

# inherits sitedev configuration
from sitedev import *

RELATIVE_URLS = False
#GOOGLE_ANALYTICS = 'UA-123456780-0'
#FEED_EMAIL = 'https://feedburner.google.com/fb/a/mailverify?uri=voraklsnotes/atom&amp;loc=en_US'
#FEED_DOMAIN = 'https://feeds.feedburner.com'
FEED_DOMAIN = 'https://vorakl.com'
FEED_ALL_ATOM = 'atom.xml'
