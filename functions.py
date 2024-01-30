from database import *
import json

def loadBannedWords() -> list:
    '''Load all need files'''
    with open('filter_banned_english.txt', 'r', encoding='UTF-8') as file:
        return file.read().split('\n')

def loadDbPhrases():
    '''Upload to database phrases (languages)'''
    with open('phrases.json', 'r', encoding='UTF-8') as file:
        DB_TG_DATABASE.insertMany('languages', json.load(file))
        print('Json "phrases.json" is loaded.')