from psycopg2 import DatabaseError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from api_university.config import Configuration
from api_university.db.tools.utils import PsqlDatabaseConnection
from api_university.db.tools.db_tools import (Database,
                                              DatabaseRole,
                                              DatabaseUser,
                                              DatabasePrivilege)

db_config = Configuration.DATABASE


def delete_db(dbname_superuser: str,
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
    WARNING!
    COMPLETE DELETION OF DATABASE TOGETHER WITH USERS!
    """
    try:
        with PsqlDatabaseConnection(dbname=dbname_superuser,
                                    user=superuser_name,
                                    password=superuser_password,
                                    host=host,
                                    port=port,
                                    isolation_level=isolation_level) as db:
            # Init db:
            existing_db = Database(dbname_user, db.connection)

            # Init role
            existing_role = DatabaseRole(role_name, db.connection)

            # Init user:
            existing_user = DatabaseUser(user_name, user_password, db.connection)

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


if __name__ == '__main__':
    delete_db(dbname_superuser="postgres",
              superuser_name="postgres",
              superuser_password="12345",
              dbname_user=db_config['db_name'],
              user_name=db_config['user_name'],
              user_password=db_config['user_password'],
              role_name=db_config['role_name'],
              host="127.0.0.1",
              port="5432")
