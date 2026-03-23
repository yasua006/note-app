import sys
from os import getenv

host: str | None = getenv("host")
port: str | None = getenv("port")
username: str | None = getenv("username")
password: str | None = getenv("password")
db_name: str | None = getenv("db_name")

if not host or not port:
    sys.exit(1)
if not username or not password:
    sys.exit(1)
if not db_name:
    sys.exit(1)

db_config: dict[str, str | int] = {
    "host": host,
    "port": int(port),
    "username": username,
    "password": password,
    "database": db_name,
    "autocommit": True
}

# * Connection string fungerer ikke på MacOS
# DATABASE_URL: str = f"mariadb://{username}:{password}@{host}:{port}/{db_name}?autocommit=true"