from dataclasses import dataclass
from psycopg2 import DatabaseError

from api_university.config import Configuration
from api_university.db.tools.utils import (
    PsqlDatabaseConnection,
    try_except_decorator
)
from api_university.db.tools.db_tools import (
    Database,
    DatabaseRole,
    DatabaseUser,
    DatabasePrivilege
)

db_config = Configuration.DATABASE


@dataclass()
class DatabaseOperation:
    connection: PsqlDatabaseConnection
    dbname: str
    user_name: str
    user_password: str
    role_name: str = None

    @try_except_decorator(DatabaseError)
    def create_db(self):
        """
        Default: Create db and user with password.

        It is also possible to create a role.
        """
        with self.connection as db:
            # Create new database:
            new_db = Database(self.dbname, db.connection)
            new_db.create_postgresql_db()

            # Create new user:
            new_user = DatabaseUser(self.user_name, self.user_password, db.connection)
            new_user.create_new_user()

            if self.role_name is not None:
                # Create new role:
                new_role = DatabaseRole(self.role_name, db.connection)
                new_role.create_new_role()
                # Assign privileges on the database to the role:
                new_role_privileges = DatabasePrivilege(new_db.db_name, new_role.role_name, db.connection)
                new_role_privileges.grant_all_privileges()
                # Join user to role:
                new_role.join_user_to_role(new_user.username)
            else:
                # Assign privileges on the database to the user:
                new_user_privileges = DatabasePrivilege(new_db.db_name, new_user.username, db.connection)
                new_user_privileges.grant_all_privileges()

    @try_except_decorator(DatabaseError)
    def delete_db(self):
        """
        WARNING!
        COMPLETE DELETION OF DATABASE TOGETHER WITH USERS AND ROLES!
        """
        with self.connection as db:
            # Init db:
            existing_db = Database(self.dbname, db.connection)

            # Init user:
            existing_user = DatabaseUser(self.user_name, self.user_password, db.connection)

            if self.role_name is not None:
                # Init role
                existing_role = DatabaseRole(self.role_name, db.connection)
                # Init role privilege:
                existing_role_privileges = DatabasePrivilege(existing_db.db_name,
                                                             existing_role.role_name,
                                                             db.connection)
                # Remove all privileges from role:
                existing_role_privileges.remove_all_privileges()
                # Remove user from role:
                existing_role.remove_user_from_role(existing_user.username)
                # Drop the role:
                existing_role.drop_role()
            else:
                # Init user privilege:
                existing_user_privileges = DatabasePrivilege(existing_db.db_name,
                                                             existing_user.username,
                                                             db.connection)
                # Remove all privileges from user:
                existing_user_privileges.remove_all_privileges()

            # Drop the db:
            existing_db.drop_postgresql_db()

            # Drop the user:
            existing_user.drop_user()


if __name__ == '__main__':
    # init connection
    conn = PsqlDatabaseConnection()

    # init database params
    database = DatabaseOperation(connection=conn,
                                 dbname=db_config['db_name'],
                                 user_name=db_config['user_name'],
                                 user_password=db_config['user_password'],
                                 role_name=db_config['role_name'])
    # db operations:
    database.create_db()
    # database.delete_db()
