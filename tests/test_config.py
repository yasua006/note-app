import sys
from os import getenv

MARIADB_HOST: str | None = getenv("MARIADB_HOST")
MARIADB_PORT: str | None = getenv("MARIADB_PORT")
MARIADB_USER: str | None = getenv("MARIADB_USER")
MARIADB_PASSWORD: str | None = getenv("MARIADB_PASSWORD")
test_db_name: str | None = getenv("test_db_name")

if not MARIADB_HOST or not MARIADB_PORT:
    sys.exit(1)
if not MARIADB_USER or not MARIADB_PASSWORD:
    sys.exit(1)
if not test_db_name:
    sys.exit(1)

db_config: dict[str, str | int] = {
    "host": MARIADB_HOST,
    "port": int(MARIADB_PORT),
    "username": MARIADB_USER,
    "password": MARIADB_PASSWORD,
    "database": test_db_name,
    "autocommit": True
}

# * Connection string fungerer ikke på MacOS
# DATABASE_URL: str = f"mariadb://{MARIADB_USER}:{MARIADB_PASSWORD}@{MARIADB_HOST}:{MARIADB_PORT}/{test_db_name}?autocommit=true"
