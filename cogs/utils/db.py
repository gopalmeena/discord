import os
import psycopg2
from .logger import logger


def db_connector(func):
    # database connection wrapper function
    def with_connection_(*args, **kwargs):
        db_config = {
        'user': os.environ.get("User"),
        'password': os.environ.get("Password"),
        'database': os.environ.get("Database"),
        'host': os.environ.get("Host"),
        'sslmode': 'allow'
        }
        conn = psycopg2.connect(**db_config)
        try:
            rv = func(conn, *args, **kwargs)
        except Exception:
            conn.rollback()
            logger.error("Database connection error")
            raise
        else:
            conn.commit()
        finally:
            conn.close()
        return rv
    return with_connection_


@db_connector
def persist_query(conn, user_id, search_query, searched_at):
    # store user's search query with user_id and timestamp
    cursor = conn.cursor()
    cursor.execute(f"Insert into user_queries(user_id, query, searched_at) " +
        f"Values('{user_id}', '{search_query}', '{searched_at}')")
    cursor.close()
    return True


@db_connector
def fetch_query(conn, user_id, search_query):
    # retrieve distinct latest queries(multiple results)
    cursor = conn.cursor()
    sql_query = f"select query from user_queries where user_id='{user_id}' and query like '%{search_query}%' order by searched_at DESC"
    cursor.execute(f"select DISTINCT queries.query from ({sql_query}) queries")
    results = cursor.fetchall()
    cursor.close()
    return results