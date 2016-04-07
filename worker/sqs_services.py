import boto3


class SqsServices:
    """
    """

    def __init__(self):
        self.sqs = boto3.resource('sqs')

    def get_queue(self, queue_name):
        return self.sqs.get_queue_by_name(QueueName=queue_name)