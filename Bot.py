import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import pprint
import json 

file = open('Config.json', 'r')
Config = json.load(file)

openai.api_key = Config["openai"]
bot = Bot(Config["token"])
dp = Dispatcher(bot)

messages=[
    {'role': 'system', 'content': 'You are...'},
    {'role': 'user', 'content': 'I am a...'},
    {'role': 'assistant', 'content': 'What you want?'}
    ]


def update(messages, role, content):
    messages.append({'role': role, 'content': content})
    return messages


@dp.message_handler()
async def send(message : types.Message):
    update(messages, 'user', message.text)
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages = messages
    )

    await message.answer(response['choices'][0]['message']['content'])

executor.start_polling(dp, skip_updates=True)