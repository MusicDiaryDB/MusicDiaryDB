#!/usr/bin/env bash

python3 ./scripts/drop.py
python3 ./scripts/create_tables.py
python3 ./scripts/populate_artists_albums_songs.py
