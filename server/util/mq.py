# @author matheus bessa
# @created_at 27.05.2019
import pika
import json
import logging
import os
from server.app import post_bot_message


class Mq:

    _queue_name = 'bot_response'
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

    def process_bot_messages(self):

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self._consume_bot_message,
            auto_ack=False
        )
        logging.info('Starting reading bot messages')
        self.channel.start_consuming()

        requeued_messages = self.channel.cancel()
        print('Requeued %i messages' % requeued_messages)
        self.conn.close()

    def _consume_bot_message(self, channel, method, properties, body):
        try:
            mq_properties = json.loads(body.decode('utf-8'))
            post_bot_message(mq_properties)
            channel.basic_ack(method.delivery_tag)
        except Exception as err:
            print(err)
            self._msg_reject(channel, method, err)

    def _msg_reject(self, channel, method, error):
        try:
            channel.basic_reject(
                delivery_tag=method.delivery_tag,
                requeue=False
            )
            logging.warning(f"Error processing msg from {self.queue_name}:")
            logging.exception(error)
        except Exception as err:
            logging.exception(err)

    def _log_rejected(self, operation, motive):
        logging.warning("--------------------------------------")
        logging.warning("Nao foi possivel processar a mensagem.")
        logging.warning("Operation rejeitada:")
        logging.warning(operation)
        logging.warning("Motivo:")
        logging.warning(motive)
        logging.warning("--------------------------------------")

    def _log_ack(self, operation):
        logging.info("--------------------------------------")
        logging.info("Iniciando processamento da mensagem.")
        logging.info("Operation:")
        logging.info(operation)
        logging.info("--------------------------------------")
