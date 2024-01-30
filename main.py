import asyncio

import aiogram.exceptions
from aiogram import *
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods.restrict_chat_member import RestrictChatMember

from random import randint, choice
from datetime import datetime, timedelta
from os import path

from database import *
from keyboards import *
from functions import *
from answerForm import *

DICT_addAdmin = dict()
DICT_removeAdmin = dict()
FILTER_BANNED_WORDS = loadBannedWords()

bot = Bot('6351427879:AAEF6LCtAU5_MqNasSe0u2wvSH1bf7dXHYg')
dp = Dispatcher()

if not DB_TG_DATABASE.findOne('languages', {'name': 'P_START1'}):
    loadDbPhrases()

@dp.message(Command('start'))
async def command_start(message: Message):
    if message.chat.type == 'private':
        if DB_TG_DATABASE.findOne('admins', {'user_id': message.from_user.id}):
            await message.answer(DB_TG_DATABASE.phrasesLoad('P_START1', message.from_user.language_code))
        else:
            await message.answer(DB_TG_DATABASE.phrasesLoad('P_START2', message.from_user.language_code))
    elif message.chat.type == 'supergroup':
        if DB_TG_DATABASE.findOne('servers', {'server_id': message.chat.id}):
            await message.answer(DB_TG_DATABASE.phrasesLoad('P_START3', message.from_user.language_code))
        else:
            for el in await bot.get_chat_administrators(message.chat.id):
                if el.status == 'creator':
                    DB_TG_DATABASE.insertOne('servers', {'owner_username': el.user.username,
                                                         'server_name': message.chat.title,
                                                         'owner_id': el.user.id,
                                                         'server_id': message.chat.id,
                                                         'language': 'en'})
                    DB_TG_DATABASE.insertOne('admins', {'username': el.user.username,
                                                        'admin_id': el.user.id,
                                                        'group': 'owner',
                                                        'server_id': message.chat.id,
                                                        'priority': 99})
                    await message.answer(f'{el.user.first_name} ({el.user.username}) {DB_TG_DATABASE.phrasesLoad("P_START4", message.from_user.language_code)}')

@dp.message(Command('help'))
async def command_help(message: Message):
    if message.chat.type == 'private':
        await message.answer(DB_TG_DATABASE.phrasesLoad('P_HELP1', message.from_user.language_code))
    elif message.chat.type == 'supergroup':
        await message.answer(DB_TG_DATABASE.phrasesLoad('P_HELP2', message.from_user.language_code))

@dp.message(Command('addadmin'))
async def command_addadmin(message: Message, state: FSMContext):
    if DB_TG_DATABASE.findOne('servers', {'owner_id': message.from_user.id}):
        if message.chat.type == 'private':
            if message.from_user.id in DICT_addAdmin:
                await message.answer(DB_TG_DATABASE.phrasesLoad('P_ALREADY_ADD_ADMIN', message.from_user.language_code), reply_markup=I_PM_CANCELADDADMIN())
            else:
                await message.answer(DB_TG_DATABASE.phrasesLoad('P_INPUT_USERNAME', message.from_user.language_code), reply_markup=I_PM_CANCELADDADMIN())
                await state.set_state(Form.Form_addAdmin1)
                DICT_addAdmin.setdefault(message.from_user.id, {})
    else:
        await message.answer(DB_TG_DATABASE.phrasesLoad('P_HAVENT_PERMS', message.from_user.language_code))

@dp.message(Form.Form_addAdmin1)
async def step_addadmin1(message: Message, state: FSMContext):
    if message.chat.type == 'private':
        if message.text.startswith('@'):
            DICT_addAdmin[message.from_user.id]['username'] = message.text[1:]
            DICT_addAdmin[message.from_user.id]['priority'] = 5

            await message.answer(f'{DB_TG_DATABASE.phrasesLoad("P_USERNAME", message.from_user.language_code)}: '
                                 f'{message.text}\n\n{DB_TG_DATABASE.phrasesLoad("P_INPUT_PRIORITY", message.from_user.language_code)}',
                                 reply_markup=I_PM_CANCELADDADMIN())
            await state.set_state(Form.Form_addAdmin2)
        else:
            await message.answer(DB_TG_DATABASE.phrasesLoad('P_WRONG_USERNAME', message.from_user.language_code), reply_markup=I_PM_CANCELADDADMIN())

@dp.message(Form.Form_addAdmin2)
async def step_addadmin2(message: Message, state: FSMContext):
    if message.chat.type == 'private':
        if message.text.isdigit():
            document = DB_TG_DATABASE.findOne('servers', {'owner_id': message.from_user.id})

            await message.answer(f'{DB_TG_DATABASE.phrasesLoad("P_USERNAME", message.from_user.language_code)} '
                                 f'{DICT_addAdmin[message.from_user.id]["username"]}\n{DB_TG_DATABASE.phrasesLoad("P_PRIORITY", message.from_user.language_code)}'
                                 f'{message.text}\n\n{DB_TG_DATABASE.phrasesLoad("P_CHOOSE_SERVER", message.from_user.language_code)}',
                                 reply_markup=I_PM_CHOOSESERVER(document['server_name']))
            await state.set_state(Form.Form_addAdmin3)
            DICT_addAdmin[message.from_user.id]['priority'] = int(message.text)
        else:
            await message.answer(DB_TG_DATABASE.phrasesLoad('P_WRONG_PRIORITY', message.from_user.language_code), reply_markup=I_PM_CANCELADDADMIN())

@dp.message(Command('removeadmin'))
async def command_removeadmin(message: Message, state: FSMContext):
    if DB_TG_DATABASE.findOne('servers', {'owner_id': message.from_user.id}):
        if message.chat.type == 'private':
            await message.answer(DB_TG_DATABASE.phrasesLoad('P_INPUT_USERNAME', message.from_user.language_code), reply_markup=I_PM_CANCELREMOVEADMIN())
            await state.set_state(Form.Form_removeAdmin1)
    else:
        await message.answer(DB_TG_DATABASE.phrasesLoad('P_HAVENT_PERMS', message.from_user.language_code))

@dp.message(Form.Form_removeAdmin1)
async def step_removeAdmin1(message: Message, state: FSMContext):
    if message.chat.type == 'private':
        if message.text.startswith('@'):
            document = DB_TG_DATABASE.findOne('servers', {'owner_id': message.from_user.id})

            await state.clear()
            await message.answer(DB_TG_DATABASE.phrasesLoad('P_CHOOSE_SERVER', message.from_user.language_code), reply_markup=I_PM_CHOOSESERVER_REMOVE_ADMIN(document['server_name']))
            DICT_removeAdmin[message.from_user.id] = {'username': message.text[1:]}
        else:
            await message.answer(DB_TG_DATABASE.phrasesLoad('P_NOT_USERNAME', message.from_user.language_code), reply_markup=I_PM_CANCELREMOVEADMIN())

@dp.message(Command('info'))
async def command_info(message: Message):
    if message.chat.type == 'supergroup':
        document = DB_TG_DATABASE.findMany('autopunish', {'server_id': message.chat.id})

        for el in await bot.get_chat_administrators(message.chat.id):
            if el.status == 'creator':
                Owner = el

        await message.answer(f'''{DB_TG_DATABASE.phrasesLoad('P_SERVER', message.from_user.language_code)} "{message.chat.title}:

{DB_TG_DATABASE.phrasesLoad('P_OWNER', message.from_user.language_code)}: @{Owner.user.username} ({Owner.user.first_name})
{DB_TG_DATABASE.phrasesLoad('P_COUNT_MESSAGES', message.from_user.language_code)}: {message.message_id}
{DB_TG_DATABASE.phrasesLoad('P_MEMBERS', message.from_user.language_code)}: {await bot.get_chat_member_count(message.chat.id)}
{DB_TG_DATABASE.phrasesLoad('P_ADMINISTRATORS', message.from_user.language_code)}: {len(await bot.get_chat_administrators(message.chat.id))}
{DB_TG_DATABASE.phrasesLoad('P_COUNT_OF_MUTES', message.from_user.language_code)}: {len(document)}''')

@dp.message(Command('unmute'))
async def command_unmute(message: Message, state: FSMContext):
    if DB_TG_DATABASE.findOne('servers', {'owner_id': message.from_user.id}):
        document_admins = DB_TG_DATABASE.findMany('admins', {'admin_id': message.from_user.id})

        for el in document_admins:
            if el['admin_id'] == message.from_user.id:
                await message.answer(DB_TG_DATABASE.phrasesLoad('P_INPUT_USERNAME', message.from_user.language_code))
                await state.set_state(Form.Form_unmute)
    else:
        await message.answer(DB_TG_DATABASE.phrasesLoad('P_HAVENT_PERMS', message.from_user.language_code))

@dp.message(Form.Form_unmute)
async def step_unmute(message: Message, state: FSMContext):
    try:
        document = DB_TG_DATABASE.findOne('autopunish', {'user_id': message.entities[0].user.id, 'muted': True})
    except AttributeError:
        document = {}

    if document:
        result = document.copy()
        result['muted'] = False
        DB_TG_DATABASE.updateDocument('autopunish', document, result)

        await bot.restrict_chat_member(message.chat.id, document['user_id'], types.ChatPermissions(
            can_send_messages=True,
            can_pin_messages=True,
            can_send_other_messages=True,
            can_send_polls=True,
            can_change_info=True,
            can_invite_users=True,
            can_send_audios=True,
            can_send_photos=True,
            can_send_videos=True,
            can_manage_topics=True,
            can_send_documents=True,
            can_send_video_notes=True,
            can_send_voice_notes=True,
            can_add_web_page_previews=True))
        await message.answer(f'{DB_TG_DATABASE.phrasesLoad("P_USER", message.from_user.language_code)} '
                             f'{message.text} {DB_TG_DATABASE.phrasesLoad("P_UNMUTED", message.from_user.language_code)}')
        await state.clear()

    else:
        await message.answer(DB_TG_DATABASE.phrasesLoad('P_USER_NOT_MUTED', message.from_user.language_code))
        await state.clear()

@dp.message(Command('flip'))
async def command_flip(message: Message):
    await message.answer(choice([DB_TG_DATABASE.phrasesLoad("P_FLIP_HEADS", message.from_user.language_code),
                                 DB_TG_DATABASE.phrasesLoad("P_FLIP_TAILS", message.from_user.language_code)]))

@dp.message(Command('roll'))
async def command_roll(message: Message):
    await message.answer(f'{DB_TG_DATABASE.phrasesLoad("P_ROLL_GAME", message.from_user.language_code)}: {randint(0,9)} {randint(0,9)} {randint(0,9)}')

@dp.callback_query()
async def query_handler(callback: types.CallbackQuery):
    if callback.data == 'ADDADMIN_END':
        if callback.from_user.id in DICT_addAdmin:
            document = DB_TG_DATABASE.findOne('servers', {'owner_id': callback.from_user.id})

            await callback.message.answer(f'{DB_TG_DATABASE.phrasesLoad("P_DONE_ADMIN", callback.from_user.language_code)}'
                                          f' @{DICT_addAdmin[callback.from_user.id]["username"]}'
                                          f' {DB_TG_DATABASE.phrasesLoad("P_LINKED", callback.from_user.language_code)}')
            DICT_addAdmin[callback.from_user.id]['server_id'] = document['server_id']
            DICT_addAdmin[callback.from_user.id]['group'] = 'admin'

            DB_TG_DATABASE.insertOne('admins', DICT_addAdmin[callback.from_user.id])
            DICT_addAdmin.pop(callback.from_user.id)
        else:
            await callback.answer(DB_TG_DATABASE.phrasesLoad("P_CANT_AGAIN", callback.from_user.language_code))

    elif callback.data == 'CANCEL_ADDADMIN':
        if callback.from_user.id in DICT_addAdmin:
            DICT_addAdmin.pop(callback.from_user.id)
            await callback.message.answer(DB_TG_DATABASE.phrasesLoad("P_PROCESS_CANCELED", callback.from_user.language_code))
        else:
            await callback.answer(DB_TG_DATABASE.phrasesLoad("P_PROCESS_ALREADY_CANCELED", callback.from_user.language_code))

    elif callback.data == 'CANCEL_REMOVEADMIN':
        if callback.from_user.id in DICT_removeAdmin:
            DICT_removeAdmin.pop(callback.from_user.id)
            await callback.message.answer(DB_TG_DATABASE.phrasesLoad("P_PROCESS_CANCELED", callback.from_user.language_code))
        else:
            await callback.answer(DB_TG_DATABASE.phrasesLoad("P_PROCESS_ALREADY_CANCELED", callback.from_user.language_code))

    elif callback.data == 'REMOVEADMIN_END':
        if callback.from_user.id in DICT_removeAdmin:
            document = DB_TG_DATABASE.findOne('servers', {'owner_id': callback.from_user.id})

            await callback.message.answer(f'{DB_TG_DATABASE.phrasesLoad("P_DONE_ADMIN", callback.from_user.language_code)}'
                                          f' {DICT_removeAdmin[callback.from_user.id]["username"]}'
                                          f' {DB_TG_DATABASE.phrasesLoad("P_REMOVED_FROM_SERVER", callback.from_user.language_code)}')

            DB_TG_DATABASE.deleteDocument('admins', {'username': DICT_removeAdmin[callback.from_user.id]['username'],
                                                     'server_id': document['server_id']})
            DICT_removeAdmin.pop(callback.from_user.id)
        else:
            await callback.answer(DB_TG_DATABASE.phrasesLoad("P_CANT_AGAIN", callback.from_user.language_code))

@dp.message()
async def echo(message: Message):
    if message.chat.type == 'supergroup':
        if not message.from_user.id in [el.user.id for el in await bot.get_chat_administrators(message.chat.id)]:
            isBadWord = False
            if message.text.lower() in FILTER_BANNED_WORDS:
                isBadWord = True
            else:
                for el in message.text.split():
                    if el.lower() in FILTER_BANNED_WORDS:
                        isBadWord = True
                        break
            if isBadWord:
                print(f'{datetime.now()} | {message.from_user.first_name} {message.from_user.username}: {message.text}')
                await message.delete()
                await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(
                    can_send_messages=False,
                    can_pin_messages=False,
                    can_send_other_messages=False,
                    can_send_polls=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_send_audios=False,
                    can_send_photos=False,
                    can_send_videos=False,
                    can_manage_topics=False,
                    can_send_documents=False,
                    can_send_video_notes=False,
                    can_send_voice_notes=False,
                    can_add_web_page_previews=False
                ))
                DB_TG_DATABASE.insertOne('autopunish', {'username': message.from_user.username,
                                                        'user_id': message.from_user.id,
                                                        'server_id': message.chat.id,
                                                        'message_text': message.text,
                                                        'mute_id': message.message_id,
                                                        'time': datetime.now() + timedelta(hours=1),
                                                        'muted': True})

                await asyncio.sleep(3600)
                await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(
                    can_send_messages=True,
                    can_pin_messages=True,
                    can_send_other_messages=True,
                    can_send_polls=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_send_audios=True,
                    can_send_photos=True,
                    can_send_videos=True,
                    can_manage_topics=True,
                    can_send_documents=True,
                    can_send_video_notes=True,
                    can_send_voice_notes=True,
                    can_add_web_page_previews=True))
                print(f'{datetime.now()} | {message.from_user.first_name} {message.from_user.username}: {message.text}')


async def main():
    document = DB_TG_DATABASE.findMany('autopunish', {'muted': True})

    for el in document:
        if datetime.now() > el['time']:
            result = el.copy()
            result['muted'] = False
            DB_TG_DATABASE.updateDocument('autopunish', el, result)

            try:
                await bot.restrict_chat_member(el['server_id'], el['user_id'], types.ChatPermissions(
                    can_send_messages=True,
                    can_pin_messages=True,
                    can_send_other_messages=True,
                    can_send_polls=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_send_audios=True,
                    can_send_photos=True,
                    can_send_videos=True,
                    can_manage_topics=True,
                    can_send_documents=True,
                    can_send_video_notes=True,
                    can_send_voice_notes=True,
                    can_add_web_page_previews=True))
            except aiogram.exceptions.TelegramBadRequest as er:
                print(er)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
