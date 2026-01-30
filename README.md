# osrsbox-api

A simple MongoDB bootstrap for OSRS (Old School RuneScape) game data. This repository provides a Docker Compose setup that:

1. Starts a MongoDB instance
2. Populates it with OSRS items, monsters, and prayers data from the [osrsbox](https://pypi.org/project/osrsbox/) package
3. Creates database indexes for efficient querying

This is a **dump database** for read-only purposes - no authentication, no API server, just data.

## Usage

### First Run (Load Data)

```bash
docker-compose up
```

This will:
- Start MongoDB on `localhost:27017`
- Check if the database is already populated
- If empty, load all OSRS data (items, monsters, prayers)
- Create indexes
- Exit the data-loader container

MongoDB continues running with your data.

### Subsequent Runs

```bash
docker-compose up
```

The data-loader detects existing data and skips loading automatically.

### Force Rebuild

To drop and reload all data:

```bash
# Edit .env and set FORCE_DATA_LOAD=true
docker-compose up --build
```

Or inline:

```bash
FORCE_DATA_LOAD=true docker-compose up --build
```

### Stop MongoDB

```bash
docker-compose down
```

## Configuration

Edit `.env` to configure:

```bash
DATABASE_NAME=osrsbox        # Database name
MONGO_PORT=27017             # MongoDB port
FORCE_DATA_LOAD=false        # Set to true to rebuild data
```

## Database Collections

The populated database contains:

- **items** - All OSRS items
- **monsters** - All OSRS monsters
- **prayers** - All OSRS prayers

## Architecture

- **mongo** - MongoDB container (no authentication)
- **data-loader** - Temporary container that populates data and exits
  - Uses Python scripts from `data-loader/` folder
  - Checks if data exists before loading
  - Can force rebuild via `FORCE_DATA_LOAD=true`

## Notes

- This is a **read-only dump database** - no security features
- Designed to provide OSRS data for other services to fetch
- The data comes from the community-maintained [osrsbox](https://github.com/osrsbox/osrsbox-db) package
