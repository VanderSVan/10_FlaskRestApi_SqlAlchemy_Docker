from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extensions import connection as psycopg2_conn
from api_report.sql_queries.pure_sql_queries import DatabaseSQLOperation
from api_report.sql_queries.pure_sql_queries import UserSQLOperation
from api_report.sql_queries.pure_sql_queries import RoleSQLOperation
from api_report.sql_queries.pure_sql_queries import PrivilegeSQLOperation
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
            cursor.execute(DatabaseSQLOperation.check_db_existence(self.db_name))
            exists, = cursor.fetchone()
            if exists:
                print(f"Database '{self.db_name}' already exists.")
            else:
                cursor.execute(DatabaseSQLOperation.create_db(self.db_name))
                print(f"Database '{self.db_name}' has been created.")

    @try_except_decorator(Error)
    def drop_postgresql_db(self):
        with self.connection.cursor() as cursor:
            cursor.execute(DatabaseSQLOperation.check_db_existence(self.db_name))
            exists, = cursor.fetchone()
            if exists:
                cursor.execute(DatabaseSQLOperation.drop_db(self.db_name))
                print(f"Database '{self.db_name}' has been successfully dropped.")
            else:
                print(f"Can not drop the db '{self.db_name}', database does not exists.")


@dataclass
class DatabaseRole:
    role_name: str
    connection: psycopg2_conn

    @try_except_decorator(Error)
    def create_new_role(self):
        with self.connection.cursor() as cursor:
            cursor.execute(RoleSQLOperation.check_role_existence(self.role_name))
            exists, = cursor.fetchone()
            if exists:
                print(f"Role '{self.role_name}' already exists.")
            else:
                cursor.execute(RoleSQLOperation.create_new_role(self.role_name))
                print(f"Role '{self.role_name}' has been created")

    @try_except_decorator(Error)
    def drop_role(self):
        with self.connection.cursor() as cursor:
            cursor.execute(RoleSQLOperation.check_role_existence(self.role_name))
            exists, = cursor.fetchone()
            print(exists)
            if exists:
                cursor.execute(RoleSQLOperation.drop_role(self.role_name))
                print(f"Role '{self.role_name}' has been successfully dropped.")
            else:
                print(f"Can not drop role '{self.role_name}', role does not exists.")

    @try_except_decorator(Error)
    def join_user_to_role(self, username: str):
        with self.connection.cursor() as cursor:
            cursor.execute(UserSQLOperation.check_membership(username))
            exists, = cursor.fetchone()
            if exists:
                print(f"User '{username}' already joined.")
            else:
                cursor.execute(RoleSQLOperation.join_user_to_role(self.role_name, username))
                print(f"User '{username}' has been successfully joined to role")

    @try_except_decorator(Error)
    def remove_user_from_role(self, username: str):
        with self.connection.cursor() as cursor:
            cursor.execute(UserSQLOperation.check_membership(username))
            exists, = cursor.fetchone()
            if exists:
                cursor.execute(RoleSQLOperation.remove_user_from_role(self.role_name, username))
                print(f"User '{username}' has been successfully removed from role")
            else:
                print(f"User '{username}' has no membership in any role")


@dataclass
class DatabaseUser:
    username: str
    password: str
    connection: psycopg2_conn

    @try_except_decorator(Error)
    def create_new_user(self):
        with self.connection.cursor() as cursor:
            cursor.execute(UserSQLOperation.check_user_existence(self.username))
            exists, = cursor.fetchone()
            if exists:
                print(f"User '{self.username}' already exists.")
            else:
                cursor.execute(UserSQLOperation.create_new_user(self.username, self.password))
                print(f"User '{self.username}' has been created")

    @try_except_decorator(Error)
    def drop_user(self):
        with self.connection.cursor() as cursor:
            cursor.execute(UserSQLOperation.check_user_existence(self.username))
            exists, = cursor.fetchone()
            if exists:
                cursor.execute(UserSQLOperation.drop_user(self.username))
                print(f"User '{self.username}' has been successfully dropped.")
            else:
                print(f"Can not drop user '{self.username}', user does not exists.")


@dataclass
class DatabasePrivilege:
    db_name: str
    role_name: str
    connection: psycopg2_conn
    
    @try_except_decorator(Error)
    def grant_all_privileges(self):
        with self.connection.cursor() as cursor:
            cursor.execute(PrivilegeSQLOperation.grant_all_privileges(self.db_name, self.role_name))

    @try_except_decorator(Error)
    def remove_all_privilege(self):
        with self.connection.cursor() as cursor:
            cursor.execute(PrivilegeSQLOperation.remove_all_privileges(self.db_name, self.role_name))


if __name__ == '__main__':
    # first connection via superuser
    with PsqlDatabaseConnection(user="postgres",
                                password="12345",
                                host="127.0.0.1",
                                port="5432",
                                isolation_level=ISOLATION_LEVEL_AUTOCOMMIT) as db:
        # Create new database:
        new_db = Database('university', db.connection)
        new_db.create_postgresql_db()

        # Create new role:
        admins_role = DatabaseRole('admins', db.connection)
        admins_role.create_new_role()

        # Privilege setting:
        admins_role_privileges = DatabasePrivilege(new_db.db_name, admins_role.role_name, db.connection)
        admins_role_privileges.grant_all_privileges()

        # Create new user:
        admin_user = DatabaseUser('admin', "1111", db.connection)
        admin_user.create_new_user()

        # Join user to role:
        admins_role.join_user_to_role(admin_user.username)

