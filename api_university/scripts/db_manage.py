import argparse

from api_university.config import Configuration
from api_university.db.tools.utils import PsqlDatabaseConnection
from api_university.db.db_operations import DatabaseOperation

db_config = Configuration.DATABASE


def create_arguments():
    parser = argparse.ArgumentParser(
        prog="creation or deletion db",
        description="available commands:",
        epilog="Try '--create_db'"
    )
    parser.add_argument('--create_db', action='store_true', help='create db')
    parser.add_argument('--delete_db', action='store_true', help='delete db')
    return parser.parse_args()


def main():
    args = create_arguments()
    # init connection
    conn = PsqlDatabaseConnection()

    # init database params
    database = DatabaseOperation(connection=conn,
                                 dbname=db_config['db_name'],
                                 user_name=db_config['user_name'],
                                 user_password=db_config['user_password'],
                                 role_name=db_config.get('role_name'))
    if args.create_db:
        database.create_db()
    elif args.delete_db:
        database.delete_db()


if __name__ == '__main__':
    main()
