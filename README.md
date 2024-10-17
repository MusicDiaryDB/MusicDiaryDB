# MusicDiaryDB

## Usage

**Database + DB monitoring via docker:**
```bash
docker compose up

# if the first command doesn't work, you have a different version of docker compose (use this instead):
docker-compose up

# Create tables
# (initialize venv if necessary)
python ./scripts/create_tables.py
```

The database will be running on port 5432, and login credentials can be found in [docker-compose.yml](docker-compose.yml).


There is an admin ui via Adminer that can be accessed from [http://localhost:8080](http://localhost:8080).
Choose postgressql from the dropdown and enter login credentials and 'music_diary_db'.

Tables can be viewed from the menu on the lefthand side.



**Python Backend and CRUD UI:**

Ensure database is running first and run the script (see setup section for more details about virtual environments if they are being used)
```bash
python ./main.py
```

The UI will be accessible from [http://localhost:5000](http://localhost:5000).

Table constraints are enforced so some table operations will require other tables to contain entries.

Use Adminer to verify that table operations are working as expected.


#### Dependencies:
- python 3.12
- python libraries as defined in [requirements.txt](requirements.txt)
- docker
- docker compose (or docker-compose)

#### Setup

Python virtual environment (name of activate file may vary slightly by operating system):
```bash
# for linux:
python3 -m venv ./.venv
source ./.venv activate
pip install -r requirements.txt
```

