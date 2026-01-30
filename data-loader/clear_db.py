#!/usr/bin/env python3
"""
Clear all collections from the MongoDB database.
"""
import pymongo
import os
import sys


def clear_database():
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
        db_name = os.environ['DATABASE_NAME']

        print(f"Dropping database: {db_name}")
        client.drop_database(db_name)
        print("Database dropped successfully.")

        return 0

    except Exception as e:
        print(f'Error clearing database: {e}')
        return 1


if __name__ == "__main__":
    sys.exit(clear_database())
