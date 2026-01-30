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
        client = pymongo.MongoClient(
            f"mongodb://{os.getenv('MONGO_HOST', 'mongo')}:{os.getenv('MONGO_PORT', '27017')}/",
            serverSelectionTimeoutMS=5000
        )
        db_name = os.getenv('DATABASE_NAME', 'osrsbox')

        print(f"Dropping database: {db_name}")
        client.drop_database(db_name)
        print("Database dropped successfully.")

        return 0

    except Exception as e:
        print(f'Error clearing database: {e}')
        return 1


if __name__ == "__main__":
    sys.exit(clear_database())
