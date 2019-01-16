import mysql.connector
import hashlib
import time 
from datetime import datetime
from datetime import timedelta

from pymongo import MongoClient
from pymongo import IndexModel, ASCENDING, DESCENDING


class MongoManager:

    def __init__(self, server_ip='localhost', client=None, expires=timedelta(days=30)):
        """
        client: mongo database client
        expires: timedelta of amount of time before a cache entry is considered expired
        """
        # if a client object is not passed 
        # then try connecting to mongodb at the default localhost port 
        self.client = MongoClient(server_ip, 27017) if client is None else client
        #create collection to store cached webpages,
        # which is the equivalent of a table in a relational database
        self.db = self.client.weibo

        # create index if db is empty
        if self.db.post.count() is 0:
            self.db.mfw.create_index([("id", ASCENDING)])

    def insert_data(self, collection_name, data):
        self.db.weibo.insert_one()

    def clear(self):
        self.db.mfw.drop()

if __name__ == '__main__':
    pass