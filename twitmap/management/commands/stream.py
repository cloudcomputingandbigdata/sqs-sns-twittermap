"""
    This module is a customized django manage.py command to use twitter
    streaming API. The command open a connection to twitter and pull tweets
    with corresponding track keywords to database or file based on options.
"""
import sys
from django.core.management.base import BaseCommand, CommandError
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


class Command(BaseCommand):
    """docstring for Command"""
    def add_arguments(self, parser):
        #positional arguments

        #optional arguments
        parser.add_argument('--output', action='store_true', dest='output', help='output tweets to twitter.txt')
        
    def handle(self, *arg, **options):
        access_token = "YOUR ACCESS TOKEN"
        access_token_secret = "YOUR ACCESS TOKEN SECRET"
        consumer_key = "CONSUMER KEY"
        consumer_secret = "CONSUMER SECRET"
        
        listener = TweetListener(**options)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, listener)
        stream.filter(track=['python', 'javascript', 'ruby'])


class TweetListener(StreamListener):
    """docstring for TweetListener"""
    def __init__(self, *arg, **options):
        if 'output' in options and options['output']:
            self.orig_stdout = sys.stdout
            self.output = file('twitter.txt', 'w')
            sys.stdout = self.output

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        sys.stdout = self.orig_stdout
        self.output.close()
        print status
        


