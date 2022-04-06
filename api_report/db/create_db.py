from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import DatabaseError
from utils import PsqlDatabaseConnection
from db_tools import Database
from db_tools import DatabaseRole
from db_tools import DatabasePrivilege
from db_tools import DatabaseUser


if __name__ == '__main__':
    # first connection via superuser
    try:
        with PsqlDatabaseConnection(dbname="postgres",
                                    user="postgres",
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

    except DatabaseError as db_error:
        print(db_error)
    except Exception as error:
        print(error)

