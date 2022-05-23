import sys
import os

from dotenv import load_dotenv
from psycopg2 import connect, OperationalError
from psycopg2.extensions import connection as psycopg2_conn, ISOLATION_LEVEL_AUTOCOMMIT
from dataclasses import dataclass

load_dotenv()


@dataclass
class PsqlDatabaseConnection:
    """Connection through superuser"""
    dbname: str = os.getenv("PG_SUPERUSER_DB")
    user: str = os.getenv("PG_SUPERUSER")
    password: str = os.getenv("PG_SUPERUSER_PASSWORD")
    host: str = os.getenv("POSTGRES_HOST")
    port: str = os.getenv("POSTGRES_PORT")
    isolation_level: int = ISOLATION_LEVEL_AUTOCOMMIT

    @staticmethod
    def print_psycopg2_exception(err):
        # get details about the exception
        err_type, err_obj, traceback = sys.exc_info()

        # get the line number when exception occured
        line_num = traceback.tb_lineno
        print("===psycopg2 exception in more detail===")
        # print the connect() error
        print("\npsycopg2 ERROR:", err, "on line number:", line_num)
        print("psycopg2 traceback:", traceback, "-- type:", err_type)

        # psycopg2 extensions.Diagnostics object attribute
        print("\nextensions.Diagnostics:", err.diag)
        print('obj=', err_obj.args)

        # print the pgcode and pgerror exceptions
        print("pgerror:", err.pgerror)
        print("pgcode:", err.pgcode)
        print("===end psycopg2 exception===\n")

    def __enter__(self):
        try:
            self.connection = connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port)
        except OperationalError as err:
            print("Error: Unable to connect!\nInput connection data is probably wrong.\n")
            self.print_psycopg2_exception(err)

        self.connection.set_isolation_level(self.isolation_level)
        print("[Postgres connection open:")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        print("Postgres connection close.]")


def _get_pure_notices(notices: list) -> str:
    if len(notices) > 1:
        pure_notices_list = [notice.split(sep=':')[1].lstrip().rstrip() for notice in notices]
        pure_result = "\n".join(pure_notices_list)
    elif len(notices) == 0:
        pure_result = ""
    else:
        pure_result = notices[0].split(sep=':')[1].lstrip().rstrip()
    return pure_result


def print_notices(notices: list):
    pure_notices = _get_pure_notices(notices)
    if len(notices) > 0:
        print('===SQL notices==\n',
              f'\n{pure_notices}\n',
              '\n===End SQL notices===')


def print_sql_error(error: Exception):
    print('===SQL error===\n',
          f'\n{error}\n',
          '\n===End SQL error===')


def try_except_decorator(error):
    def outer_wrapper(func):
        def inner_wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except error as err:
                print_sql_error(err)
            except Exception as default_err:
                print(f"Got an exception: {default_err}")
                print('Type exception =', type(default_err))
            finally:
                if isinstance(self.connection, psycopg2_conn):
                    print_notices(self.connection.notices)

        return inner_wrapper

    return outer_wrapper
