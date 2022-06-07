# Task 10 - Flask RESTful (SqlAlchemy(PSql), Marshmallow, Docker) 
## Tags:

- `Flask-restful`
- `PostgreSQL`
- `SqlAlchemy`
- `Docker`
- `Marshmallow`
- `Migrations`
- `Swagger`

## Description:
0) **API URL = http://localhost/api/v1**
1) **Create an application that inserts/updates/deletes data in the database using `sqlalchemy`
and `flask rest framework`;**

2) **Use `PostgreSQL` DB;**

3) **Models have to have next fields:**

   1. GroupModel:
      - name

   2. StudentModel:
      - group_id
      - first_name
      - last_name

   3. CourseModel:
      - name
      - description;
4) **Migrations must be done with `flask-migrate`;**
5) **Serialization and deserialization should be done with `marshmallow` or `flask-marshmallow`;**
6) **Create a wrapper module (package) for SQL queries in python that:**
   - Creates user, role and database.
   - Assigns all privileges on the database to the role/user;
7) Create cli for create / drop db with params such as: user, role, db;

8) **Create a python application**
   - Generate test data:
     + 10 groups with randomly generated names. *The name should contain 2 characters, hyphen, 2 numbers
       (example: AA-11);*
     + Create 10 courses (*math, biology, etc*);
     + 200 students. *Take 20 first names and 20 last names and randomly combine them to generate students*;

   - Randomly assign students to groups. *Each group could contain from 10 to 30 students;
     It is possible that some groups will be without students or students without groups*;
   - Create relation MANY-TO-MANY between tables STUDENTS and COURSES.
     *Randomly assign from 1 to 3 courses for each student*;
   
   - Write SQL queries using `sqlalchemy` or `flask-sqlalchemy`:
     + Find all groups with less or equals student count;
     + Find all students related to the course with a given course_id;
     + Add a student to the course (from a list);
     + Remove the student from one of his or her courses;
     + CRUD operation for student / student list;
     + CRUD operation for group;
     + CRUD operation for course.

   - Modify application using `Flask Rest Framework`;
   - Write tests using `Unittest` module or `pytest`.

9) Resources:
   - SQLalchemy https://www.sqlalchemy.org/
# Installation:
## Installation via Docker-compose:
### 1. For the beginning install `docker` and `docker compose` on your machine:
1) [docker](https://docs.docker.com/engine/install/ubuntu/)
2) [docker-compose](https://docs.docker.com/compose/install/)
3) P.S.: Depending on the version use:
    ```commandline
    docker compose
    ```
   Or
    ```commandline
    docker-compose
    ```

### 2. Then `git clone` this project in your folder.
### 3. Go to the folder where are `docker-compose.yml` and `Dockerfile` are located.
### 4. Now use following command:
- default mode (production mode)
   ```commandline
   docker compose build
   ```
- If you want to run in development mode, then:
   ```commandline
   docker compose -f docker-compose.dev.yml build
   ```
### 5. After image building, you can up the containers of one of these commands:
- default mode:
   ```commandline
   docker compose up
   ```
- background mode:
   ```commandline
   docker compose up -d
   ```
### 6. Try to get data:
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
### 7. You can get api docs by entering the url into your browser:
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
### 8. If you use development mode, you can run pytest:
- First, enter to the container:
    ```commandline
    docker exec -it api bash
    ```
- Second, run `pytest` command:
    ```bash
    cd tests/ && python3 -m pytest
    ```
### 9. If you need:
- to stop the containers only:
   ```commandline
    docker compose stop
    ```
- to stop and remove the containers:
   ```commandline
    docker compose down
   ```

### 10. Remove all container data:
1) remove images:
    ```commandline
        docker rmi postgres 10_flaskrestapi_sqlalchemy_docker_api python:3.10-slim-buster
    ```
2) remove volumes:
    ```commandline
        docker volume rm 10_flaskrestapi_sqlalchemy_docker_myapp 10_flaskrestapi_sqlalchemy_docker_psql_db
    ```

### 11. Possible errors:
- if you get `postgres` warnings after app started,
then you should probably change outer port for `postgres` in `docker-compose.yml`:
   ```yaml
   ports:
         - '5432:5432'
  
   # changed to
  
   ports:
         - '5632:5432'
   ```
- if you got something like this:
   ```commandline
   Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock:...
   ```

   Use:
   ```commandline
   sudo chmod 666 /var/run/docker.sock
   ```
- if you use ubuntu, then you will probably have a problems with psycopg2.
So install this:
    ```commandline
    sudo apt-get install libpq-dev
    ```
## Installation via IDE or other:
### 1) Create env and install packages:
```commandline
pip install pipenv
```
```commandline
pipenv shell
```
```commandline
pipenv install
```
Or
```commandline
pipenv install --dev
```


### 2) For start api:
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
### 3) Get docs and data in your browser:
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

# Migrations:
### 1) If you begin only and have no database and have no migrations folder:
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
### 2) If you want update models only:
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