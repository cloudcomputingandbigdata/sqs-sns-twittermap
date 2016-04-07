from alchemyapi import AlchemyAPI

class SentimentAnalyzer:
    def __init__(self):
        self.alchemyapi = AlchemyAPI()

    def get_sentiment(self, text):
        response = self.alchemyapi.sentiment("text", text)
        # print response
        if response['status'] == 'OK':
            return response["docSentiment"]["type"]
        else:
            # print response['statusInfo']
            return 'none'
