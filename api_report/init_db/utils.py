from psycopg2 import connect
from dataclasses import dataclass


@dataclass
class PsqlDatabaseConnection:
    user: str
    password: str
    host: str
    port: str
    isolation_level: int

    def __enter__(self):
        self.connection = connect(user=self.user,
                                  password=self.password,
                                  host=self.host,
                                  port=self.port)
        print("PostgreSQL connection open.")
        self.connection.set_isolation_level(self.isolation_level)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        print("PostgreSQL connection close.")


def get_pure_notices(notices: list) -> str:
    if len(notices) > 1:
        pure_notices_list = [notice.split(sep=':')[1].lstrip().rstrip() for notice in notices]
        pure_result = "\n".join(pure_notices_list)
    elif len(notices) == 0:
        pure_result = ""
    else:
        pure_result = notices[0].split(sep=':')[1].lstrip().rstrip()
    return pure_result


# for Tests
# print(get_pure_notices(['ЗАМЕЧАНИЕ:  Database mydb already exists\n',
#                         'ЗАМЕЧАНИЕ:  Database mydb already exists\n',
#                         'ЗАМЕЧАНИЕ:  Database mydb already exists\n']))
#
# print(get_pure_notices([]))
#
# print(get_pure_notices(['ЗАМЕЧАНИЕ:  Database mydb already exists\n']))


def print_notices(notices: list):
    pure_notices = get_pure_notices(notices)
    if len(notices) > 0:
        print('===SQL notices==\n',
              f'\n{pure_notices}\n',
              '\n===End SQL notices===')


def print_sql_error(error: Exception):
    print('===SQL error===\n',
          f'\n{error}\n',
          '\n===End SQL error===')


# print_notices(['ЗАМЕЧАНИЕ:  Database mydb already exists\n',
#                'ЗАМЕЧАНИЕ:  Database mydb already exists\n',
#                'ЗАМЕЧАНИЕ:  Database mydb already exists\n'])


def try_except_decorator(error):
    def outer_wrapper(func):
        def inner_wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except error as err:
                print_sql_error(err)
            except Exception as default_err:
                print(f"Get Exception {default_err}")
            finally:
                print_notices(self.connection.notices)

        return inner_wrapper

    return outer_wrapper

