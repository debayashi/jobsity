from server.util.mq import Mq
from threading import Thread
import logging
import pika
from time import sleep

logging.getLogger("pika").setLevel(logging.WARNING)


class BotConsumerThread(Thread):
    def run(self):
        sleep_time = 15
        while True:
            try:
                mq = Mq()
                mq.process_bot_messages()
            except pika.exceptions.ConnectionClosedByBroker:
                logging.error(
                    "Connection closed by broker."
                    "Reconnecting..."
                )
                sleep(sleep_time)
                continue
            except pika.exceptions.AMQPChannelError:
                logging.error(
                    "Channel Error."
                    "Reconnecting..."
                )
                sleep(sleep_time)
                continue
            except pika.exceptions.AMQPConnectionError:
                logging.error(
                    "Queue connection error."
                    "Reconnecting..."
                )
                sleep(sleep_time)
                continue
