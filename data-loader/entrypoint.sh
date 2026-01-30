#!/bin/sh
set -e

echo "DEBUG: FORCE_DATA_LOAD = '$FORCE_DATA_LOAD'"
echo "DEBUG: DATABASE_NAME = '$DATABASE_NAME'"

# If FORCE_DATA_LOAD is true, clear the database
if [ "$FORCE_DATA_LOAD" = "true" ]; then
    echo "FORCE_DATA_LOAD=true, clearing database..."
    python3 /scripts/clear_db.py || true
fi

# Check if database has data
echo "Checking if database has data..."
python3 /scripts/check_db_populated.py
DB_CHECK=$?

# If database has data, skip loading
if [ $DB_CHECK -eq 2 ]; then
    echo "Database already populated. Exiting."
    exit 0
fi

# Load data
echo "Loading data into database..."
python3 /scripts/mongo_insert_osrsbox.py

echo "Creating database indexes..."
python3 /scripts/mongo_index_database.py

echo "Data insertion and indexing complete."
