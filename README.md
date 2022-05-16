# Task_10_PSQL_Rest_API

**Installation:**

- if you use ubuntu, then you will have a problems with psycopg2.
So install this:
```commandline
sudo apt-get install libpq-dev
```
Or
```commandline
pipenv run pip install psycopg2
```

- create env and install packages:
```commandline
pip install pipenv
pipenv shell
pipenv install
```

For start api:
```
$env:FLASK_APP = 'app.py'
flask db init
flask db migrate
```