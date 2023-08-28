from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from tokens import token_1

HELP_COMMAND = """
/start - начать работу с ботом
/help - список команд
/description - описание бота
/contacts - контакт создателя
/end - завершить работу с ботом
"""

API_TOKEN: str = token_1

bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer(text='Your bot was started')
    message.delete()


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=HELP_COMMAND)


@dp.message(Command(commands=['description']))
async def process_description_command(message: Message):
    await message.answer(text='<em>This is an Echo-bot, that can work'
                         'with <b>different types</b> of data.</em>',
                         parse_mode="HTML")


@dp.message(Command(commands=['contacts']))
async def process_contacts_command(message: Message):
    await message.answer(text='@grigoriy_tashu')

# @dp.message(Command(commands=['end']))
# async def process_end_command(message: Message):
    # await Message(text='ending')


@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
        # print(message.model_dump_json(indent=4))
    except TypeError:
        await message.reply(text='This type of apdates is not supported'
                            'by the "send_copy" method.')


if __name__ == '__main__':
    dp.run_polling(bot)
