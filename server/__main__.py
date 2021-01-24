from server.app import run_server
from server.util.bot_msg_consumer import BotConsumerThread

if __name__ == '__main__':
    BotConsumerThread(name='BotConsumerThread').start()
    run_server()
