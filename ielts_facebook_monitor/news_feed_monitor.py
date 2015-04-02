
import collections
import re

from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message
import requests
import transaction


class NewsFeedMonitor(object):
    ''' Methods to get posts from a news feed and flag by keyword '''

    def __init__(self, access_token, search_fields, keywords, mail_settings=None,
                 mail_targets=None):
        self.access_token = access_token
        self.search_fields = search_fields
        self.keywords = keywords
        self.regex_get_keywords = re.compile("[\w']+")
        self.processed_posts = collections.Counter()
        self.keyword_frequency = collections.Counter()
        self.run_count = 0
        self.failure_count = 0
        if mail_settings is not None:
            self.mailer = Mailer.from_settings(mail_settings)
            self.mail_settings = mail_settings
            self.mail_targets = mail_targets
        else:
            self.mailer = None
            self.mail_settings = None
            self.mail_targets = None

    def get_feed_posts(self):
        ''' get json news feed using read_stream API '''
        request = requests.get(
            'https://graph.facebook.com/v2.3/me/home', params={
                'access_token': self.access_token, 'format': 'json',
                'filter': 'owner'})
        if 'data' not in request.json():
            raise ValueError('Failed authentication')
        return request.json()['data']

    def get_post_keywords(self, post):
        ''' return a counter of keywords from selected fields '''
        keyword_counter = collections.Counter()
        for field in self.search_fields:
            if field not in post:
                continue
            keyword_counter.update(
                self.regex_get_keywords.findall(post[field]))
        return keyword_counter

    def flag_post(self, post):
        ''' return whether a post should be flagged based on the monitor setup
        '''
        post_keywords = self.get_post_keywords(post)
        for keyword in self.keywords:
            if keyword in post_keywords:
                return True
        return False

    def read_news_feed(self):
        ''' read new posts from the feed and return flagged posts '''
        self.run_count += 1
        try:
            posts = self.get_feed_posts()
        except ValueError:
            self.failure_count += 1
            return []
        # successfully retrieved news feed: process posts
        flagged_posts = []
        for post in posts:
            if post['id'] not in self.processed_posts:
                # not seen before - process this post
                keyword_counter = self.get_post_keywords(post)
                # count the number of posts each keyword appears in
                self.keyword_frequency.update(keyword_counter.keys())
                self.processed_posts.update([post['id']])
                # check for flags
                if self.flag_post(post):
                    flagged_posts.append(post)
        return flagged_posts

    def mail_post(self, post):
        ''' send a post as an email '''
        if self.mailer is None:
            raise ValueError('Mailer not configured')
        message = Message(
            subject='NewsFeedMonitor flagged a post',
            sender=self.mail_settings['mail.username'],
            recipients=self.mail_targets, body=str(post))
        self.mailer.send(message)
        transaction.commit()

    def watch_task(self):
        ''' process the news feed and email flagged posts '''
        for flagged_post in self.read_news_feed():
            self.mail_post(flagged_post)
