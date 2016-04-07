from sns_services import *
from sqs_services import *
from sentiment_analyzer import *
import json

sns = SnsServices()
sqs = SqsServices()
sentiment_analyzer = SentimentAnalyzer()

topic = sns.create_or_get_topic('twittermap')
queue = sqs.get_queue('twitterMap')

if __name__ == '__main__':
    print 'Worker starts...'
    while True:
        for message in queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20):
            try:
                tweet = json.loads(message.body)
                contents = tweet['text']
                print 'contents: ' + contents
                sentiment = sentiment_analyzer.get_sentiment(contents)
                tweet['sentiment'] = sentiment
                print 'sentiment: ' + sentiment
                tweet = json.dumps(tweet, ensure_ascii=False)
                topic.publish(Message=tweet)
            except Exception as e:
                print e
            finally:
                message.delete()