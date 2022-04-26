from psycopg2 import DatabaseError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from api_university.config import Configuration
from api_university.db.utils import PsqlDatabaseConnection
from api_university.db.db_operations import (Database,
                                             DatabaseRole,
                                             DatabaseUser,
                                             DatabasePrivilege)

db_config = Configuration.DATABASE


def create_db(dbname_superuser: str,
              superuser_name: str,
              superuser_password: str,
              dbname_user: str,
              user_name: str,
              user_password: str,
              role_name: str,
              host: str,
              port: str,
              isolation_level=ISOLATION_LEVEL_AUTOCOMMIT):
    """
    First connection through superuser.
    """
    try:
        with PsqlDatabaseConnection(dbname=dbname_superuser,
                                    user=superuser_name,
                                    password=superuser_password,
                                    host=host,
                                    port=port,
                                    isolation_level=isolation_level) as db:
            # Create new database:
            new_db = Database(dbname_user, db.connection)
            new_db.create_postgresql_db()

            # Create new role:
            admins_role = DatabaseRole(role_name, db.connection)
            admins_role.create_new_role()

            # Privilege setting:
            admins_role_privileges = DatabasePrivilege(new_db.db_name, admins_role.role_name, db.connection)
            admins_role_privileges.grant_all_privileges()

            # Create new user:
            admin_user = DatabaseUser(user_name, user_password, db.connection)
            admin_user.create_new_user()

            # Join user to role:
            admins_role.join_user_to_role(admin_user.username)

    except DatabaseError as db_error:
        print(db_error)
    except Exception as error:
        print(error)


if __name__ == '__main__':
    create_db(dbname_superuser="postgres",
              superuser_name="postgres",
              superuser_password="12345",
              dbname_user=db_config['db_name'],
              user_name=db_config['user_name'],
              user_password=db_config['user_password'],
              role_name=db_config['role_name'],
              host="127.0.0.1",
              port="5432")
