from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Format - KeyboardType_ChatType_Keyboard
#
# SG - SuperGroup
# PM - PrivateMessage
#
# I - Inline
# K - Default Keyboard

def I_PM_CHOOSESERVER(server:str):
    '''return keyboard with text (server name)'''
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=server, callback_data='ADDADMIN_END'),
                                                  InlineKeyboardButton(text='Cancel', callback_data='CANCEL_ADDADMIN')]])

def I_PM_CHOOSESERVER_REMOVE_ADMIN(server:str):
    '''return keyboard with text (server name)'''
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=server,
                                                                       callback_data='REMOVEADMIN_END'),
                                                  InlineKeyboardButton(text='Cancel',
                                                                       callback_data='CANCEL_REMOVEADMIN')]])

def I_PM_CHOOSEINFOSERVER(server:str):
    '''return keyboard with text (server name)'''
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=server,
                                                                       callback_data='INFOSERVER')]])

def I_PM_CANCELADDADMIN():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Cancel',
                                                                       callback_data='CANCEL_ADDADMIN')]])

def I_PM_CANCELREMOVEADMIN():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Cancel',
                                                                       callback_data='CANCEL_REMOVEADMIN')]])
