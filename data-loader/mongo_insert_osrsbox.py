import itertools
import time

import pymongo
from osrsbox import items_api
from osrsbox import monsters_api
from osrsbox import prayers_api

from connection_properties import ConnectionProperties
cp = ConnectionProperties()

# Retry connection logic to wait for MongoDB to be ready
max_retries = 30
retry_count = 0
client = None

while retry_count < max_retries:
    try:
        client = pymongo.MongoClient(
            f"mongodb://{cp.host}:{cp.port}/",
            serverSelectionTimeoutMS=5000
        )
        client.server_info()
        print("  > Connected to MongoDB successfully")
        break
    except (pymongo.errors.ServerSelectionTimeoutError, pymongo.errors.OperationFailure):
        retry_count += 1
        print(f"  > Waiting for MongoDB... (attempt {retry_count}/{max_retries})")
        time.sleep(2)

if client is None:
    print("Failed to connect to MongoDB after retries")
    exit(1)

db = client[cp.db_name]


def insert_data(db_type: str):
    print(f">>> Inserting {db_type} data...")

    if db_type == "items" or db_type == "icons_items":
        all_db_entries = items_api.load()
    elif db_type == "monsters":
        all_db_entries = monsters_api.load()
    elif db_type == "prayers" or db_type == "icons_prayers":
        all_db_entries = prayers_api.load()

    all_entries = list()
    bulk_entries = list()

    for entry in all_db_entries:
        if "icons" in db_type:
            new_entry = dict()
            new_entry["id"] = entry.id
            new_entry["icon"] = entry.icon
            entry = new_entry.copy()
        all_entries.append(entry)

    collection = db[db_type]
    collection.delete_many({})

    for db_entries in itertools.zip_longest(*[iter(all_entries)] * 50):
        db_entries = filter(None, db_entries)
        db_entries = list(db_entries)
        bulk_entries.append(db_entries)

    for i, block in enumerate(bulk_entries):
        print(f"  > Processed: {i*50}")
        to_insert = list()
        for entry in block:
            if not isinstance(entry, dict):
                entry = entry.construct_json()
            to_insert.append(entry)

        collection = db[db_type]
        collection.insert_many(to_insert)


if __name__ == "__main__":
    dbs = ["items", "monsters", "prayers", "icons_items", "icons_prayers"]
    for db_type in dbs:
        insert_data(db_type)
        collection = db[db_type]
        print(">>> Indexing...")
        collection.create_index("_id")
        if db_type in ["items", "monsters"]:
            collection.create_index([("name", pymongo.TEXT)], default_language="english")