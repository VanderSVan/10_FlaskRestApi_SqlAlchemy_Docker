import argparse

from api_university.db.db_operations import DatabaseOperation


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

    # init database
    database = DatabaseOperation()

    # db operations:
    if args.create_db:
        database.create_db()
    elif args.delete_db:
        database.delete_db()


if __name__ == '__main__':
    main()
