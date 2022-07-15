# REST-API UNIVERSITY
## Project uses:

- `Flask (flask-restful)`
- `SqlAlchemy (flask-sqlalchemy)`
- `PostgreSQL`
- `Migrations (flask-migrate)`
- `Marshmallow (flask-marshmallow)`
- `Swagger (flasgger)`
- `Docker (docker-compose)`
- `Pytest`

## Task description:
To get rest-api docs, visit [http://0.0.0.0:5000/api/v1](http://0.0.0.0:5000/api/v1)

<details>
<summary>Main stack:</summary>

1) **Create an application that inserts/updates/deletes data in the database using `sqlalchemy`
and `flask rest framework`;**
2) **Use `PostgreSQL` DB;**
3) **Migrations must be done with `flask-migrate`;**
4) **Serialization and deserialization should be done with `marshmallow` or `flask-marshmallow`;**
</details>

<details>
<summary>Models:</summary>

**Models should have the following fields:**
   1. GroupModel:
      - name

   2. StudentModel:
      - group_id
      - first_name
      - last_name

   3. CourseModel:
      - name
      - description;
</details>
      
<details>
<summary>Wrapper for SQL queries:</summary>

**Create a wrapper module (package) for SQL queries in python that:**
   - Creates user, role and database.
   - Assigns all privileges on the database to the role/user;
</details>
   
<details>
<summary>CLI:</summary>

**Create cli for create / drop db with params such as: user, role, db;**
</details>

<details>
<summary>Generate test data:</summary>

- 10 groups with randomly generated names. *The name should contain 2 characters, hyphen, 2 numbers
  (example: AA-11);*
  - Create 10 courses (*math, biology, etc*);
  - 200 students. *Take 20 first names and 20 last names and randomly combine them to generate students*;
  - Randomly assign students to groups. *Each group could contain from 10 to 30 students;
    It is possible that some groups will be without students or students without groups*;
</details>

<details>
<summary>Database:</summary>

Create relation MANY-TO-MANY between tables STUDENTS and COURSES.
  *Randomly assign from 1 to 3 courses for each student*;
   1) Write SQL queries using `sqlalchemy` or `flask-sqlalchemy`:
      + Find all groups with less or equals student count;
      + Find all students related to the course with a given course_id;
      + Add a student to the course (from a list);
      + Remove the student from one of his or her courses;
      + CRUD operation for student / student list;
      + CRUD operation for group;
      + CRUD operation for course.
</details>

<details>
<summary>Other:</summary>

- Modify application using `Flask Rest Framework`;
- Write tests using `Unittest` module or `pytest`.
</details>

   
## Installation:
First you need to create `.env` file with environment variables at the root of the project, that contains:
```
POSTGRES_DB = superuser_database_name (by default: postgres)
POSTGRES_USER = superuser_login (by default: postgres)
POSTGRES_PASSWORD = superuser_password (by default: postgres)
PG_HOST = host_url (by default: localhost)
PG_PORT = postgres_port  (by default: 5432)
PG_DB = your_database_name (by default: university)
PG_ROLE = your_role_name
PG_USER = your_user_name
PG_USER_PASSWORD = your_user_password
```

Or you can set these variables yourself.


### Installation via Docker-compose:

<details>
<summary>STEP 1 - Install docker and docker compose:</summary>

**For the beginning install `docker` and `docker compose` on your machine:**
1) **[docker](https://docs.docker.com/engine/install/ubuntu/)**
2) **[docker-compose](https://docs.docker.com/compose/install/)**
3) **P.S.: Depending on the version use:**
    ```commandline
    docker compose
    ```
   Or
    ```commandline
    docker-compose
    ```
</details>

<details>
<summary>STEP 2 - Git clone:</summary>

1) **Then `git clone` this project in your folder.**
2) **And go to the folder where are `docker-compose.yml` and `Dockerfile` are located.**
</details>

<details>
<summary>STEP 3 - Build project:</summary>

**Use following command:**
- default mode (production mode)
   ```commandline
   docker compose build
   ```
- Or if you want to run in development mode:
   ```commandline
   docker compose -f docker-compose.dev.yml build
   ```
</details>

<details>
<summary>STEP 4 - Up the containers:</summary>

**After image building, you can up the containers of one of these commands:**
- default mode:
   ```commandline
   docker compose up
   ```
- background mode:
   ```commandline
   docker compose up -d
   ```
</details>

<details>
<summary>STEP 5 - Try to get data:</summary>

```commandline
curl http://localhost/api/v1/students/10
```
Or
```commandline
curl http://127.0.0.1:5000/api/v1/students/10
```
Or
```commandline
curl http://0.0.0.0:5000/api/v1/students/10
```
</details>

<details>
<summary>STEP 6 - Get api docs in your browser:</summary>

 - **[http://localhost/api/v1](http://localhost/api/v1)**

    Or

 - **[http://127.0.0.1:5000/api/v1](http://127.0.0.1:5000/api/v1)**

    Or

 - **[http://0.0.0.0:5000/api/v1](http://0.0.0.0:5000/api/v1)**
</details>

<details>
<summary>STEP 7 - Run pytest:</summary>

**If you use development mode, you can run pytest:**
- First, enter to the container:
    ```commandline
    docker exec -it api bash
    ```
- Second, run `pytest` command:
    ```bash
    cd tests/ && python3 -m pytest
    ```
</details>

<details>
<summary>STEP 8 - Stop and remove containers:</summary>

**If you need:**
- to stop the containers only:
   ```commandline
    docker compose stop
    ```
- to stop and remove the containers:
   ```commandline
    docker compose down
   ```
</details>

<details>
<summary>STEP 9 - Remove all containers data:</summary>

1) remove images:
    ```commandline
    docker rmi postgres 10_flaskrestapi_sqlalchemy_docker_api python:3.10-slim-buster
    ```
2) remove volumes:
    ```commandline
    docker volume rm 10_flaskrestapi_sqlalchemy_docker_myapp 10_flaskrestapi_sqlalchemy_docker_psql_db
    ```
</details>

<details>
<summary>POSSIBLE ERRORS:</summary>

- **if you get `postgres` warnings after app started,
then you should probably change outer port for `postgres` in `docker-compose.yml`:**
    ```yaml
    ports:
      - '5432:5432'
    ```
   *change to ↓*
    ```yaml
    ports:
      - '5632:5432'
    ```
- **if you got something like this:**
   ```commandline
   Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock:...
   ```
   *Use:*
   ```commandline
   sudo chmod 666 /var/run/docker.sock
   ```
- **if you use ubuntu, then you will probably have a problems with psycopg2.
So install this:**
    ```commandline
    sudo apt-get install libpq-dev
    ```
</details>

### Installation via IDE or other:

<details>
<summary>STEP 1 - Create env and install packages:</summary>

1) ```commandline
    pip install pipenv
    ```
2) ```commandline
   pipenv shell
   ```
3) ```commandline
   pipenv install
   ```
    Or
   ```commandline
    pipenv install --dev
   ```
</details>

<details>
<summary>STEP 2 - Start api:</summary>

- `Ubuntu` (`Bash`):
    ```bash
    export PG_HOST=0.0.0.0 &&
    cd api_university/ &&
    export FLASK_APP=app.py &&
    flask run
    ```
- `Windows` (`PowerShell`):
   ```commandline
   cd api_university/
   $env:FLASK_APP = 'app.py'
   flask run
   ```
- `CMD`:
   ```commandline
   cd api_university/
   set FLASK_APP=app.py
   flask run
   ```
</details>

<details>
<summary>STEP 3 - Get api docs:</summary>

**Get docs and data in your browser:**
```
http://localhost/api/v1
```
Or
```
http://127.0.0.1:5000/api/v1
```
Or
```
http://0.0.0.0:5000/api/v1
```
</details>

## Migrations:

<details>
<summary>If you begin only and have no database and have no migrations folder:</summary>

**Get docs and data in your browser:**
- `Ubuntu` (`Bash`):
   ```bash
    cd api_university/
    python3 -m scripts --create_db
    export FLASK_APP = 'app.py'
    flask db init
    flask db migrate
    flask db upgrade
    ```
- `Windows` (`PowerShell`):
    ```commandline
    cd api_university/
    py -m scripts --create_db
    $env:FLASK_APP = 'app.py'
    flask db init
    flask db migrate
    flask db upgrade
    ```
</details>

<details>
<summary>If you want update models only:</summary>

- `Ubuntu` (`Bash`):
    ```bash
    cd api_university/
    export FLASK_APP = 'app.py'
    flask db migrate
    flask db upgrade
    ```
- `Windows` (`PowerShell`):
    ```commandline
    cd api_university/
    $env:FLASK_APP = 'app.py'
    flask db migrate
    flask db upgrade
    ```
</details>

## CLI
**Simple command line interface, that:**

1) allows you to create db:
   ``` commandline
   py -m api_university.scripts --create_db
   ```
2) allows you to drop db:
   ``` commandline
   py -m api_university.scripts --drop_db
   ```
3) And contains optional arguments:
    - `-d`, `--db_name`, allows assign db name:
   
        ``` commandline
        py -m api_university.scripts --drop_db -d your_db_name
        ```

    - `-u`, `--user_name`, allows assign username:
   
        ``` commandline
        py -m api_university.scripts --create_db -r your_user_name
        ```
    
    - `-r`, `--role_name`, allows assign role name:
   
        ``` commandline
        py -m api_university.scripts --create_db -r your_role_name
        ```
    
    - `-p`, `--user_password`, allows assign user password:
   
        ``` commandline
        py -m api_university.scripts --create_db -p your_user_password
        ```


**IMPORTANT:** **If the arguments is not specified, it is taken from the env variables or set by default.**