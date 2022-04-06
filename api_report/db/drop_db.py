from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import DatabaseError
from utils import PsqlDatabaseConnection
from db_tools import Database
from db_tools import DatabaseRole
from db_tools import DatabasePrivilege
from db_tools import DatabaseUser


if __name__ == '__main__':
    ####################!!! WARNING !!!####################
    # !!! COMPLETE DELETION OF DATABASE TOGETHER WITH USERS !!!
    try:
        with PsqlDatabaseConnection(dbname="postgres",
                                    user="postgres",
                                    password="12345",
                                    host="127.0.0.1",
                                    port="5432",
                                    isolation_level=ISOLATION_LEVEL_AUTOCOMMIT) as db:
            # Init db:
            existing_db = Database('university', db.connection)

            # Init role
            existing_role = DatabaseRole('admins', db.connection)

            # Init user:
            existing_user = DatabaseUser('admin', "1111", db.connection)

            # Init role privilege:
            existing_role_privileges = DatabasePrivilege(existing_db.db_name,
                                                         existing_role.role_name,
                                                         db.connection)

            # Remove all privileges from role:
            existing_role_privileges.remove_all_privileges()

            # Drop the db:
            existing_db.drop_postgresql_db()

            # Remove user from role:
            existing_role.remove_user_from_role(existing_user.username)

            # Drop the user:
            existing_user.drop_user()

            # Drop the role:
            existing_role.drop_role()

    except DatabaseError as db_error:
        print(db_error)
    except Exception as error:
        print(error)


