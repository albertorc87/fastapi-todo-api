import os
os.environ['RUN_ENV'] = 'test'

from app.v1.model import user_model, todo_model
from app.v1.utils.settings import Settings

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

settings = Settings()


def postgresql_connection():
    con = psycopg2.connect(f"user='{settings.db_user}' password='{settings.db_pass}'")
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return con

def delete_database():

    if not settings.db_name.startswith("test_"):
        raise Exception(f'Invalid name for database = {settings.db_name}')

    sql_drop_db = f"DROP DATABASE IF EXISTS {settings.db_name}"
    con = postgresql_connection()
    cursor = con.cursor()
    cursor.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE  pg_stat_activity.datname = '{settings.db_name}' AND pid <> pg_backend_pid();")
    cursor.execute(sql_drop_db)
    con.close()

def create_database():
    sql_create_db = f"CREATE DATABASE {settings.db_name} WITH OWNER = {settings.db_user} ENCODING = 'UTF8' CONNECTION LIMIT = -1;"

    con = postgresql_connection()
    cursor = con.cursor()
    cursor.execute(sql_create_db)
    con.close()

def pytest_sessionstart(session):

    delete_database()
    create_database()

    from app.v1.utils.db import db

    with db:
        db.create_tables([user_model.User, todo_model.Todo])


def pytest_sessionfinish(session, exitstatus):
    delete_database()

