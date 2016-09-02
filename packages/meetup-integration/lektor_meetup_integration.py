# -*- coding: utf-8 -*-
import io
import os
import os.path
import json
import requests
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
        print("Setting up Meetup.com integration")
        key = os.environ.get('MEETUP_API_KEY')
        if not key:
            print("No MEETUP_API_KEY found. Not importing data")
        self.api_key = key
        self._load_rsvp_cache()

    def on_before_build(self, source, **extra):
        if not self.api_key:
            return
        if isinstance(source, Page):
            if source['_model'] == 'event':
                start = source['start']
                now = datetime.datetime.now()
                if source['groups']:
                    for group in source['groups'].blocks:
                        group._data['rsvps'] = self._get_reservations(unicode(group['url']), cached_only=(start >= now))
        self._save_rsvp_cache()

    def on_process_template_context(self, context, **extra):
        def test_function():
            return 'Value from plugin %s' % self.name
        context['test_function'] = test_function

    def _load_rsvp_cache(self):
        cache_file = '_meetup_rsvp_cache.json'
        if os.path.exists(cache_file):
            with io.open(cache_file, encoding='utf-8') as fp:
                data = json.load(fp)
                self.rsvp_cache = data

    def _save_rsvp_cache(self):
        cache_file = '_meetup_rsvp_cache.json'
        with open(cache_file, 'w+') as fp:
            json.dump(self.rsvp_cache, fp)


    def _get_reservations(self, url, cached_only=True):
        """
        This retrieves the number of reservations for events either from a
        cache (valid for 10 minutes) or from meetup.com

        If cached_only is set, the age of the cache is ignored. As long as
        there is a cached value, it will be used.
        """
        elements = url.split('/')
        if len(elements) < 6:
            return None
        group_name = elements[3]
        event_id = elements[5]
        cache_key = u'{}:{}'.format(group_name, event_id)
        result = self.rsvp_cache.get(cache_key)
        now = datetime.datetime.utcnow()
        if result is not None:
            ts = datetime.datetime.utcfromtimestamp(result['_ts'])
            if not cached_only and ts + datetime.timedelta(minutes=10) > now:
                return result
        req_url = "https://api.meetup.com/{group_name}/events/{event_id}?key={key}".format(group_name=group_name, event_id=event_id, key=self.api_key)
        data = requests.get(req_url).json()
        cache = {
            'yes': data.get('yes_rsvp_count', 0),
            'limit': data.get('rsvp_limit', 0),
            '_ts': time.time(),
        }
        self.rsvp_cache[cache_key] = cache
        return cache
