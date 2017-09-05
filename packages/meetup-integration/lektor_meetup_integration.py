# -*- coding: utf-8 -*-
import io
import os
import os.path
import json
import collections
import time
import datetime

from lektor.pluginsystem import Plugin
from lektor.db import Page


class MeetupIntegrationPlugin(Plugin):
    name = u'meetup-integration'
    description = u'Add your description here.'
    api_key = None
    rsvp_cache = {}

    def on_setup_env(self, **extra):
        self.whitelist = set()

    def on_after_build_all(self, builder):
        with io.open(os.path.join('assets', 'whitelist.txt'), 'w') as fp:
            for item in self.whitelist:
                fp.write(u'{}\n'.format(item))

    def on_before_build(self, source, **extra):
        if isinstance(source, Page):
            if source['_model'] == 'event':
                start = source['start']
                now = datetime.datetime.now()
                if source['groups']:
                    for group in source['groups'].blocks:
                        url = unicode(group._data.get('url', ''))
                        if 'https://www.meetup.com' in url:
                            self.whitelist.add(url)
