
import configparser
import operator
import time

from news_feed_monitor import NewsFeedMonitor


def get_monitor():
    credentials = configparser.ConfigParser()
    credentials.read('credentials.ini')
    smtp_settings = configparser.ConfigParser()
    smtp_settings.read('gmail_smtp.ini')

    mail_settings = {
        'mail.host': smtp_settings['mail']['host'],
        'mail.port': smtp_settings['mail']['port'],
        'mail.ssl': smtp_settings['mail']['ssl'],
        'mail.username': credentials['mail']['username'],
        'mail.password': credentials['mail']['password']}
    access_token = credentials['facebook']['access_token']
    send_to = credentials['mail']['send_to']

    monitor = NewsFeedMonitor(
        access_token=access_token, keywords=['cats', 'cat', 'life'],
        search_fields=['message', 'description', 'caption', 'story'],
        mail_settings=mail_settings, mail_targets=[send_to])

    return monitor


def run_watcher_once():
    monitor = get_monitor()
    monitor.watch_task()


def collect_feed_stats():
    monitor = get_monitor()

    for i in range(10):
        flags = monitor.read_news_feed()
        if flags:
            for post in flags:
                print('Flagged: ', post['id'])
        print('{iter} complete'.format(iter=i+1))
        time.sleep(60)

    for row in reversed(sorted(
            monitor.keyword_frequency.items(), key=operator.itemgetter(1))):
        print(row)

    print('Processed posts: ', len(monitor.processed_posts))


def run_watcher_continuous(delay, iterations):
    monitor = get_monitor()
    for i in range(iterations):
        monitor.watch_task()
        time.sleep(delay)


if __name__ == '__main__':
    run_watcher_continuous(60, 60)
