from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from tokens import echo_token

HELP_COMMAND = """
/start - start working with the bot
/help - list commands
/description - description of the bot's work
/stat - view statistic
/contacts - creator's contact
/end - quit the bot
"""

API_TOKEN: str = echo_token

users: dict = {}

bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Your bot was started.\n'
                         'You can send him anything.')
    message.delete()
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': True,
                                       'total_messages': 0,
                                       'total_games': 1}
    else:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['total_games'] += 1
    print(message.from_user.first_name)
    print(message.from_user.last_name)


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=HELP_COMMAND)


@dp.message(Command(commands=['description']))
async def process_description_command(message: Message):
    await message.answer('<em>This is an Echo-bot, that can work '
                         'with <b>different types</b> of data.</em>'
                         '\nIt gives you back everything you send him.',
                         parse_mode="HTML")


@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(f'In total, you played {users[message.from_user.id]["total_games"]} times\n\n'
                         f'This game you sent {users[message.from_user.id]["total_messages"]} messages')


@dp.message(Command(commands=['contacts']))
async def process_contacts_command(message: Message):
    await message.answer(text='@grigoriy_tashu')


@dp.message(Command(commands=['end']))
async def process_end_command(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        users[message.from_user.id]['total_messages'] = 0
        await message.answer('Your game is over!')
    else:
        await message.answer('Your game hasn\'t started.'
                             '\n\nPress /start')


async def send_sticker_echo(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer_sticker(message.sticker.file_id)
        users[message.from_user.id]['total_messages'] += 1
    else:
        await message.answer('You are not in game. \n'
                             'Please, press /start')

dp.message.register(send_sticker_echo, F.sticker)


@dp.message()
async def send_echo(message: Message):
    if users[message.from_user.id]['in_game']:
        try:
            await message.send_copy(chat_id=message.chat.id)
            users[message.from_user.id]['total_messages'] += 1
        # print(message.model_dump_json(indent=4))
        except TypeError:
            await message.reply(text='This type of updates is not supported'
                                'by the "send_copy" method.')
            users[message.from_user.id]['total_messages'] += 1
    else:
        await message.answer('You are not in game. \n'
                             'Please, press /start')


if __name__ == '__main__':
    dp.run_polling(bot)
