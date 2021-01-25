# Jobsity Coding Challenge

This project consists of a simple browser-based chat application developed in Python.

**Implementation**

The chat app uses sockets in the clients-server communication. 

**Future improvements**

* Add to support to multiple chat rooms
* Add more bot commands
* Improve error messages and exception handling.

## Usage


The module requires Python 3+. If needed, configure a virtualenv on the project folder.

> `virtualenv venv -p python3`
> `source venv/bin/active`

This project has two main functionalities: the server and the chat bot. The server is located in the 'server' folder. And the chat bot in the bot_server folder.
Each one of them have their own requirements.txt.

> `pip install -r requirements.txt`


This application makes use o MongoDb and RabbitMq. The credentials for them must be in enviroment variables.

To run the application is suggested to use a simple shell script that exports the variables and run the app:

Server:
```
export MONGODB_URL=localhost:27017
export MONGODB_USER=user
export MONGODB_PASS=pass
export MONGODB_AUTH_SOURCE=auth-source
export MONGODB_DB=mongodb
export MONGODB_AUTH_MECANISM='SCRAM-SHA-256'

export RABBITMQ_USER=user
export RABBITMQ_PASSWORD=pass
export RABBITMQ_HOST=localhost

export SECRET_KEY='secret!'

python -m server
```

Chat Bot:
```
export RABBITMQ_USER=rabbitmq
export RABBITMQ_PASSWORD=rabbitmq
export RABBITMQ_HOST=localhost

python -m bot_server
```


## Authors

* **Thiago Kobayashi**
