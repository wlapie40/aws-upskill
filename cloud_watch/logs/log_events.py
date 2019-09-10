from resources import _client
from database import logger
import os

##todo logger decorator


class Logger:
    def __init__(self):
        self.client = _client('logs')
        self.log_group_name = f'/aws/sfigiel/{os.environ["FLASK_ENV"]}/flask'

    def describe_log_groups(self, limit=10, group_name='/aws/sfigiel/'):
        response = self.client.describe_log_groups(
            logGroupNamePrefix=group_name,
            # nextToken='string',
            limit=limit
        )
        logger.info(f'call describe_log_groups() => {response}')
        return response

    def create_log_stream(self, log_stream_name='sfigiel-test'):
        response = self.client.create_log_stream(
            logGroupName=self.log_group_name,
            logStreamName=log_stream_name
        )
        logger.info(f'call create_log_stream. Log stream: {log_stream_name} has been created')

    def create_log_group(self):
        try:
            response = self.client.create_log_group(
                logGroupName=self.log_group_name,
            )
            logger.info(f'call create_log_group(): log group has been created {response}')
        except Exception as e:
            logger.error(f'{e}')

    def put_log_events(self):
        try:
            response = self.client.put_log_events(
                    logGroupName='/aws/sfigiel/flask',
                    logStreamName='string',
                    logEvents=[
                        {
                            'timestamp': 123,
                            'message': 'test'
                        },
                    ],
                    sequenceToken='string'
                )
            print(response)
        except Exception as e:
            logger.error(f'{e}')
            self.create_log_group()
