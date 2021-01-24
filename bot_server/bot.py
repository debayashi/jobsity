import requests
import csv
from bot_server.util.mq import Mq


class Bot:

    def get_stock(self, stock):
        stock_csv = requests.get(
            f'https://stooq.com/q/l/?s={stock}&f=sd2t2ohlcv&h&e=csv​'
        )
        decoded_content = stock_csv.content.decode('utf-8')
        reader = csv.reader(decoded_content.splitlines(), delimiter=',')
        next(reader)
        return next(reader)

    def handle_stock_command(self, command):
        stock = command.split('=')[-1]
        stock_data = self.get_stock(stock)
        mq = Mq()
        stock_msg = f'{stock_data[0]} quote is {stock_data[-2]} per share'
        mq.write_bot_message('stock', stock_msg)
        mq.write_bot_message('stock', stock_msg)
