# Lift Station Navigator

![liftstation-app project banner](docs/project-banner.webp)

A field operations web application by Jason Edwards for finding lift stations and opening their coordinates in Google Maps. This repository is a cleaned portfolio edition of a recovered project archive.

## Features

- Search station numbers and street or site names as you type.
- Read station information from a PostgreSQL database through a FastAPI endpoint.
- Open a station location in Google Maps, or show “NO GPS” when coordinates are missing.
- Run the application with Docker Compose and an Nginx reverse proxy.
- Optionally geocode a locally supplied station address file with geopy and OpenStreetMap Nominatim.

## Architecture

Nginx serves the HTML/CSS/JavaScript frontend and forwards `/api/stations` to FastAPI. The API queries PostgreSQL over the Compose network. PostgreSQL retains records in a named volume. An optional Adminer service provides local database administration.

## Run locally

Requires Docker Engine or Docker Desktop with Docker Compose v2.

```bash
cd backend
cp .env.example .env
# Edit .env and replace DB_PASS with a unique password.
docker compose up --build -d
```

Open http://localhost:8102. Three fictional records are seeded on the first database startup. The coordinate pair `(0, 0)` demonstrates the map link; it is not a real station location. The database initialization script runs only when the database volume is first created.

```bash
# Check the API
curl http://localhost:8102/api/stations
# View logs
docker compose logs api
# Stop services while retaining database records
docker compose down
# Optional database administration at http://localhost:8100
docker compose --profile tools up -d
```

For Adminer, use PostgreSQL, server `db`, database `liftstations_data`, user `lift_mechanic`, and the password from your local `.env`.

## Optional address import

Create `backend/api/liftstations.txt` locally, using one record per line:

```text
LS 1: YOUR STATION ADDRESS
LS 2: ANOTHER STATION ADDRESS
```

The importer assumes Titusville, Florida when composing geocoder queries. It sends those addresses to OpenStreetMap Nominatim and uses a 1.5-second request interval. Review the provider's current usage policy and only submit addresses you are permitted to share. The input file is ignored by Git.

```bash
cd backend
docker compose exec api python import_stations.py
```

Records without a geocoder match are reported and skipped. Review coordinates before relying on navigation. The importer uses the numeric portion of a station ID as its key, so `LS 1` and `P 1` would collide; use distinct numeric IDs.

## Portfolio restoration notes

The recovered source contained the API, frontend, Compose configuration, reverse proxy, and geocoding scripts. This edition retains the Compose-served application and adds a database schema, fictional seed data, a Dockerfile, environment-based credentials, safer frontend text rendering, and these instructions. Duplicate legacy entry points, real station addresses and coordinate corrections, Python caches, the container backup, and original Git history are excluded.

This is an independent portfolio project, with no claim of City endorsement. It is a local demonstration without authentication; the published ports bind to localhost. A public deployment would require separate access controls, TLS, and operational review. Dependencies are currently unpinned.

## Validation

Python syntax and configuration structure were checked during preparation. Full Docker startup and end-to-end database integration have not been verified in the preparation environment.
