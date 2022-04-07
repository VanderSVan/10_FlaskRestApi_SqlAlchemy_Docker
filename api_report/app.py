from flask import Flask
from api_report.db.data_insertion_into_db import insert_data_to_db


def create_app(test_config=False):
    application = Flask(__name__)

    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    application.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://admin:1111@localhost:5432/university"

    @application.before_first_request
    def create_tables():
        db.create_all()

        insert_data_to_db(db)

        db.session.commit()
        print('Tables has been created')

    if test_config:
        application.config['TESTING'] = True
    return application


if __name__ == '__main__':
    from api_report.db.db_sqlalchemy import db

    app = create_app()
    db.init_app(app)
    app.run(debug=True)

