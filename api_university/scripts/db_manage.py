import os
import argparse
from dotenv import load_dotenv

from api_university.db.db_operations import DatabaseOperation
from api_university.db.tools.utils import PsqlDatabaseConnection

load_dotenv()


def create_arguments():
    parser = argparse.ArgumentParser(
        prog="Creation or deletion db",
        description="By default info is taken from env variables.",
        epilog="Try '--create_db'"
    )
    parser.add_argument('-d', '--db_name', type=str, metavar="", default=None,
                        help='assign db name')
    parser.add_argument('-u', '--user_name', type=str, metavar="", default=None,
                        help='assign user name')
    parser.add_argument('-p', '--user_password', type=str, metavar="", default=None,
                        help='assign user password')
    parser.add_argument('-r', '--role_name', type=str, metavar="", default=None,
                        help='assign role name')
    parser.add_argument('--create_db', action='store_true', help='create db with params')
    parser.add_argument('--drop_db', action='store_true', help='delete db with all params')
    return parser.parse_args()


def main():
    args = create_arguments()
    with PsqlDatabaseConnection() as conn:
        # db operations:
        if args.db_name or args.user_name or args.user_password or args.role_name:
            # init database
            database = DatabaseOperation(connection=conn,
                                         db_name=args.db_name,
                                         user_name=args.user_name,
                                         user_password=args.user_password,
                                         role_name=args.role_name)
            if args.create_db:
                database.create_all()
            elif args.drop_db:
                database.drop_all()
        else:
            # init database
            database = DatabaseOperation(connection=conn,
                                         db_name=os.getenv("PG_DB"),
                                         user_name=os.getenv("PG_USER"),
                                         user_password=os.getenv("PG_USER_PASSWORD"),
                                         role_name=os.getenv("PG_ROLE"))
            if args.create_db:
                database.create_all()
            elif args.drop_db:
                database.drop_all()


if __name__ == '__main__':
    main()
