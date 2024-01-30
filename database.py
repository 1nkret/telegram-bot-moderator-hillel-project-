from pymongo import *
import pymongo.errors

class myDatabase:
    def __init__(self, name: str):
        self.name = name

    def insertOne(self, table: str, content: dict):
        '''Insert one dictionary to your database.
        :table: select table
        :content: what we need to insert (one dictionary)'''
        with MongoClient() as db:
            connectionDB = db[self.__name]

            newTable = connectionDB[table]

            try:
                newTable.insert_one(content)
            except pymongo.errors.DuplicateKeyError as err:
                print(err)


    def insertMany(self, table: str, content: list):
        '''Insert many dictionaries to your database.
        :table: select table
        :content: what we need to insert (we can insert many dictionaries)'''
        with MongoClient() as db:
            connectionDB = db[self.__name]

            newTable = connectionDB[table]
            try:
                newTable.insert_many(content)
            except pymongo.errors.DuplicateKeyError as err:
                print(err)

    def createIndex(self, table: str, n: str, u=False):
        '''Create new index to your database.
        :table: select table
        :n: name of index
        :u: is it unique?'''
        with MongoClient() as db:
            connectionDB = db[self.__name]

            newTable = connectionDB[table]
            newTable.create_index(n, unique=u)

    def findOne(self, table: str, obj: dict) -> dict:
        '''Find one object on database.
        :table: select table
        :obj: what we need to find (example: {"username": "Inkret"})
        :return: dictionary'''
        with MongoClient() as db:
            connectionDB = db[self.__name]

            return connectionDB[table].find_one(obj)

    def findMany(self, table: str, obj: dict) -> list:
        '''Find many objects on database
        :table: select table
        :obj: what we need to find (example: {"username": "Inkret"})
        :return: dictionary'''
        with MongoClient() as db:
            connectionDB = db[self.__name]

            return list(connectionDB[table].find(obj))

    def updateDocument(self, table: str, f: dict, update_data: dict):
        '''Update a document in the database
        :table: select table
        :f: filter produli to find the document to update
        :update_data: data to update in the document'''
        with MongoClient() as db:
            connectionDB = db[self.__name]

            connectionDB[table].update_one(f, {"$set": update_data})

    def deleteDocument(self, table: str, f: dict):
        '''Delete a document from the database
        :table: select table
        :f: filter criteria to find the document to delete
        '''
        with MongoClient() as db:
            connectionDB = db[self.__name]

            connectionDB[table].delete_one(f)

    def phrasesLoad(self, phrase:str, lang='en') -> str:
        '''Load languages and phrases from database.
        :phrase: name of phrase
        :lang: (message.from_user.language_code)
        :return: phrase on user language'''
        with MongoClient() as db:
            connectionDB = db[self.__name]

            return connectionDB['languages'].find_one({'name': phrase})[lang]

    @property
    def name(self) -> str:
        '''getter __name database'''
        return self.__name

    @name.setter
    def name(self, n: str):
        '''setter __name database (Do not touch!!!)'''
        self.__name = n

DB_TG_DATABASE = myDatabase('TG_BOT')
DB_TG_DATABASE.createIndex('admins', 'username', True)
DB_TG_DATABASE.createIndex('servers', 'chat_id', True)
DB_TG_DATABASE.createIndex('autopunish', 'mute_id', True)