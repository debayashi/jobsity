from server import app
from server.util.bot_msg_consumer import BotConsumerThread

if __name__ == '__main__':
    BotConsumerThread(name='BotConsumerThread').start()
    app.run_server()
