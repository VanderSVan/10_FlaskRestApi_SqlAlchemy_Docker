from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extensions import connection as psycopg2_conn
from api_report.sql_queries.pure_sql_queries import DatabaseOperation
from api_report.sql_queries.pure_sql_queries import UserOperation
from utils import PsqlDatabaseConnection
from utils import try_except_decorator
from dataclasses import dataclass


@dataclass
class Database:
    db_name: str
    connection: psycopg2_conn

    @try_except_decorator(Error)
    def create_postgresql_db(self):
        with self.connection.cursor() as cursor:
            cursor.execute(DatabaseOperation.check_db_existence(self.db_name))
            exists, = cursor.fetchone()
            if exists:
                print(f"Database '{self.db_name}' already exists.")
            else:
                cursor.execute(DatabaseOperation.create_db(self.db_name))
                print(f"Database '{self.db_name}' has been created.")
            # cursor.execute(DatabaseOperation.check(db_name))

    @try_except_decorator(Error)
    def drop_postgresql_db(self):
        with self.connection.cursor() as cursor:
            cursor.execute(DatabaseOperation.check_db_existence(self.db_name))
            exists, = cursor.fetchone()
            if exists:
                cursor.execute(DatabaseOperation.drop_db(self.db_name))
                print(f"Database '{self.db_name}' has been successfully dropped.")
            else:
                print(f"Can not drop the db '{self.db_name}', database does not exists.")
                # cursor.execute(DatabaseOperation.check(db_name))


@dataclass
class DatabaseUser:
    username: str
    password: str
    connection: psycopg2_conn

    @try_except_decorator(Error)
    def create_new_user(self):
        with self.connection.cursor() as cursor:
            cursor.execute(UserOperation.check_user_existence(self.username))
            exists, = cursor.fetchone()
            if exists:
                print(f"User '{self.username}' already exists.")
            else:
                cursor.execute(UserOperation.create_new_user(self.username, self.password))
                print(f"User '{self.username}' has been created")

    @try_except_decorator(Error)
    def drop_user(self):
        with self.connection.cursor() as cursor:
            cursor.execute(UserOperation.check_user_existence(self.username))
            exists, = cursor.fetchone()
            if exists:
                cursor.execute(UserOperation.drop_user(self.username))
                print(f"User '{self.username}' has been successfully dropped.")
            else:
                print(f"Can not drop user '{self.username}', user does not exists.")


if __name__ == '__main__':
    with PsqlDatabaseConnection(user="postgres",
                                password="12345",
                                host="127.0.0.1",
                                port="5432",
                                isolation_level=ISOLATION_LEVEL_AUTOCOMMIT) as db:
        # Create new user:
        test_user = DatabaseUser('test', '1111', db.connection)
        test_user.create_new_user()
        # Or drop user:
        # test_user.drop_user()

        # Create db.
        test_db = Database('testdb', db.connection)
        test_db.create_postgresql_db()
        # Or drop db.
        # test_db.drop_postgresql_db()
