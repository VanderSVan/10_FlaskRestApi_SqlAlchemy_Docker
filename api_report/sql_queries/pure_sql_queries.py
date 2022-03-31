from psycopg2.sql import SQL


class DatabaseOperation:
    @staticmethod
    def check_db_existence(db_name: str):
        return SQL(f"SELECT COUNT(*) = 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")

    @staticmethod
    def create_db(db_name: str):
        return SQL(f"CREATE DATABASE {db_name}")

    @staticmethod
    def drop_db(db_name: str):
        return SQL(f"DROP DATABASE {db_name}")

    # @staticmethod
    # def check(db_name: str):
    #     return f"""
    #                 DO
    #                 $do$
    #                 BEGIN
    #                    IF EXISTS (SELECT FROM pg_database WHERE datname = '{db_name}') THEN
    #                       RAISE NOTICE 'Database already exists';  -- optional
    #                    END IF;
    #                 END
    #                 $do$;
    #             """


class UserOperation:
    @staticmethod
    def check_user_existence(username: str):
        return SQL(f"SELECT COUNT(*)=1 FROM pg_roles WHERE rolname = '{username}'")

    @staticmethod
    def create_new_user(username: str, password: str):
        return SQL(f"CREATE USER {username} WITH PASSWORD '{password}'")

    @staticmethod
    def drop_user(username: str):
        return SQL(f"DROP USER IF EXISTS {username}")

    # @staticmethod
    # def check(username: str):
    #     return f"""
    #                 DO
    #                 $do$
    #                 BEGIN
    #                    IF EXISTS (SELECT COUNT(*)=1 FROM pg_roles WHERE rolname = '{username}') THEN
    #                       RAISE NOTICE 'User already exists';  -- optional
    #                    END IF;
    #                 END
    #                 $do$;
    #             """
