#!/usr/bin/env python3
"""
Check if the MongoDB database is already populated with data.

Exit codes:
    0 - Database is empty or doesn't exist (proceed with loading)
    2 - Database is already populated (skip loading)
    1 - Error occurred
"""
import pymongo
import os
import sys


def check_database():
    try:
        # Connect to MongoDB
        username = os.environ['MONGO_USERNAME']
        password = os.environ['MONGO_PASSWORD']
        host = os.environ['MONGO_HOST']
        port = os.environ['MONGO_PORT']

        client = pymongo.MongoClient(
            f"mongodb://{username}:{password}@{host}:{port}/?authSource=admin",
            serverSelectionTimeoutMS=5000
        )
        db = client[os.environ['DATABASE_NAME']]

        # Check if items collection exists and has data
        if 'items' in db.list_collection_names():
            count = db['items'].count_documents({})
            if count > 0:
                print(f'Database already populated with {count} items.')
                return 2

        print('Database is empty or not initialized.')
        return 0

    except Exception as e:
        print(f'Error checking database: {e}')
        return 1


if __name__ == "__main__":
    sys.exit(check_database())
