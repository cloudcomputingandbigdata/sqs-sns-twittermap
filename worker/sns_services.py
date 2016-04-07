import boto3


class SnsServices:
    """
    references: https://boto3.readthedocs.org/en/latest/reference/services/sns.html"
    """

    def __init__(self):
        self.sns = boto3.resource('sns')

    def create_or_get_topic(self, topic):
        response = self.sns.create_topic(
            Name=topic
        )
        return response

    def subscribe(self, topic, endpoint):
        response = topic.subscribe(Protocol='http', Endpoint=endpoint)
        print response

