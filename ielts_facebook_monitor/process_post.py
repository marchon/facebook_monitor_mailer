
import configparser
import collections
from operator import itemgetter
import re

import requests


credentials = configparser.ConfigParser()
credentials.read('credentials.ini')
API_TOKEN = credentials['facebook']['access_token']

params = {
    'access_token': API_TOKEN,
    'format': 'json',
    'filter': 'owner'
}

request = requests.get('https://graph.facebook.com/v2.3/me/home', params=params)
news_feed = request.json()['data']

key_counters = collections.defaultdict(collections.Counter)
post_counters = collections.defaultdict(int)

for post in news_feed:
    key_counters[post['type']].update(post.keys())
    post_counters[post['type']] += 1

for post_type, key_counter in key_counters.items():
    print()
    print(post_type, post_counters[post_type])
    for row in reversed(sorted(key_counter.items(), key=itemgetter(1))):
        print(row)

regex = re.compile("[\w']+")

post_meta = []
for post in news_feed:
    tmp = collections.Counter()
    for field in ['message', 'description', 'caption', 'story']:
        if field not in post:
            continue
        tmp.update(regex.findall(post[field]))
    post_meta.append(tmp)

import ipdb; ipdb.set_trace()
