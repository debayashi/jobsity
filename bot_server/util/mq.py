import pika
import json
import logging
import os
import datetime


class Mq:
    _queue_durable = True

    def __init__(self):
        try:
            rabbitmq_user = os.environ['RABBITMQ_USER']
            rabbitmq_password = os.environ['RABBITMQ_PASSWORD']
            rabbitmq_host = os.environ['RABBITMQ_HOST']
            credentials = pika.PlainCredentials(
                rabbitmq_user,
                rabbitmq_password
            )
            parameters = pika.ConnectionParameters(
                host=rabbitmq_host,
                credentials=credentials
            )
            self._conn = pika.BlockingConnection(parameters)
            self.channel = self._conn.channel()
            self._queue_name = 'bot_response'
            self._queue_declare(self._queue_name)
        except pika.exceptions.AMQPConnectionError:
            logging.error("Error connecting to RabbitMQ")
            raise

    @property
    def conn(self):
        return self._conn

    @property
    def queue_name(self):
        return self._queue_name

    @property
    def queue_durable(self):
        return self._queue_durable

    def write_bot_message(self, command, msg):
        
        rabbit_msg = {
            'command': command,
            'msg': msg,
            'date': str(datetime.datetime.now())

        }
        body = json.dumps(rabbit_msg).encode('utf-8')
        self.channel.basic_publish(
            exchange=self._queue_name+'_ex',
            routing_key=self._queue_name,
            body=body
        )

    def _queue_declare(self, queue_name):

        # Creates the queue exchange
        self.channel.exchange_declare(
            exchange=queue_name+'_ex',
            exchange_type='direct'
        )

        # Creates the queue dead letter exchange
        self.channel.exchange_declare(
            exchange=queue_name+'_dlx',
            exchange_type='fanout'
        )

        # Creates the request main queue
        self.channel.queue_declare(
            queue=queue_name,
            durable=self.queue_durable,
            arguments={
                "x-dead-letter-exchange": queue_name+'_dlx'
            }
        )

        self.channel.queue_bind(
            exchange=queue_name+'_ex',
            queue=queue_name
        )

        # Creates a dead letter queue
        self.channel.queue_declare(
            queue=queue_name+'_dl',
            durable=self.queue_durable
        )

        self.channel.queue_bind(
            exchange=queue_name+'_dlx',
            queue=queue_name+'_dl'
        )
