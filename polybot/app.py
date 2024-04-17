import json
import telebot
from loguru import logger
import os
import requests

YOLO_URL = f'http://yolo5:8081'


class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token, threaded=False)
        self.bot.set_update_listener(self._bot_internal_handler) 
        self.current_msg = None

    def _bot_internal_handler(self, messages):
        """Bot internal messages handler"""
        for message in messages:
            self.current_msg = message
            self.handle_message(message)

    def start(self):
        """Start polling msgs from users, this function never returns"""
        logger.info(f'{self.__class__.__name__} is up and listening to new messages....')
        logger.info(f'Telegram Bot information\n\n{self.bot.get_me()}')
        self.bot.infinity_polling()

    def send_text(self, text):
        self.bot.send_message(self.current_msg.chat.id, text)

    def send_text_with_quote(self, text, message_id):
        self.bot.send_message(self.current_msg.chat.id, text, reply_to_message_id=message_id)

    def is_current_msg_photo(self):
        return self.current_msg.content_type == 'photo'

    def download_user_photo(self, quality=2):
        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)
        :param quality: integer representing the file quality. Allowed values are [0, 1, 2]
        :return:
        """
        if not self.is_current_msg_photo():
            raise RuntimeError(
                f'Message content of type \'photo\' expected, but got {self.current_msg.content_type}')

        file_info = self.bot.get_file(self.current_msg.photo[quality].file_id)
        data = self.bot.download_file(file_info.file_path)
        folder_name = file_info.file_path.split('/')[0]

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    def handle_message(self, message):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {message}')
        self.send_text(f'Your original message: {message.text}')


class QuoteBot(Bot):
    def handle_message(self, message):
        logger.info(f'Incoming message: {message}')

        if message.text != 'Please don\'t quote me':
            self.send_text_with_quote(message.text, message_id=message.message_id)


class ObjectDetectionBot(Bot):
    def __init__(self, token):
        super().__init__(token)
        self.api_key = self.read_api_key_from_file('.apikey')

    @staticmethod
    def read_api_key_from_file(file_path):
        with open(file_path, 'r') as f:
            api_key = f.read().strip()
        return api_key

    def handle_message(self, message):
        if message.text == '':
            self.send_text("Press Enter to start...")
        elif message.text == 'start':
            self.send_text("Press 1 for India news\nPress 2 for International news\nPress 3 for Business news\nPress 4 for Sports news")
        elif message.text in ['1', '2', '3', '4']:
            category = ''
            country = ''
            if message.text == '1':
                category = 'general'
                country = 'in'
            elif message.text == '2':
                category = 'general'
                country = 'us'
            elif message.text == '3':
                category = 'business'
                country = 'us'
            elif message.text == '4':
                category = 'sports'
                country = 'us'

            response = requests.get(f'https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={self.api_key}')

            if response.status_code == 200:
                data = response.json()
                articles = data['articles'][:5]  # Fetch the first 5 articles

                if articles:
                    for article in articles:
                        title = article['title']
                        description = article['description']
                        article_url = article['url']  # Extract the article URL
                        message_text = f"{title}\n{description}\n{article_url}"
                        self.send_text(message_text)

                    self.send_text("Press 1 for India news\nPress 2 for International news\nPress 3 for Business news\nPress 4 for Sports news")  # Send options again
                else:
                    self.send_text('No articles found.')
                    self.send_text("Press 1 for India news\nPress 2 for International news\nPress 3 for Business news\nPress 4 for Sports news")  # Send options again
            else:
                self.send_text(f"Request failed with status code: {response.status_code}")
                self.send_text("Press 1 for India news\nPress 2 for International news\nPress 3 for Business news\nPress 4 for Sports news")  # Send options again
        else:
            self.send_text("Invalid input. Please try again.")
            self.send_text("Press 1 for India news\nPress 2 for International news\nPress 3 for Business news\nPress 4 for Sports news")  # Send options again

        logger.info(f'Incoming message: {message}')


if __name__ == '__main__':
    with open('.telegramToken') as f:
        _token = f.read()

    my_bot = ObjectDetectionBot(_token)
    my_bot.start()
