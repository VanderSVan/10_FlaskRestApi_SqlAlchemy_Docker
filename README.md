# Task 10 - Flask RESTful (Rest api, SqlAlchemy, Docker) 
## Tags:

- `Flask-restful`
- `PostgreSQL`
- `SqlAlchemy`
- `Docker`
- `Marshmallow`
- `Swagger`

##Description:
1) **Create an application that inserts/updates/deletes data in the database using `sqlalchemy` and `flask rest framework`.**

2) **Use `PostgreSQL` DB.**

3) **Models have to have next field:**

   1) GroupModel:
      - name

   2) StudentModel:
      - group_id
      - first_name
      - last_name

   3) CourseModel:
      - name
      - description
4) **Models should be created by `marshmallow` or `flask-marshmallow`**
5) **Create a wrapper module (package) for SQL queries in python that:**
   - Creates user, role and database.
   - Assigns all privileges on the database to the role/user.

6) **Create a python application**
   - Generate test data:
     + 10 groups with randomly generated names. *The name should contain 2 characters, hyphen, 2 numbers (example: AA-11)*
     + Create 10 courses (*math, biology, etc*)
     + 200 students. *Take 20 first names and 20 last names and randomly combine them to generate students.*

   - Randomly assign students to groups. *Each group could contain from 10 to 30 students. It is possible that some groups will be without students or students without groups*
   - Create relation MANY-TO-MANY between tables STUDENTS and COURSES. *Randomly assign from 1 to 3 courses for each student*
   
   - Write SQL queries using `sqlalchemy` or `flask-sqlalchemy`:
     + Find all groups with less or equals student count;
     + Find all students related to the course with a given course_id;
     + Add a student to the course (from a list);
     + Remove the student from one of his or her courses;
     + CRUD operation for student / student list;
     + CRUD operation for group;
     + CRUD operation for course.

   - Modify application using `Flask Rest Framework`.
   - Write tests using `Unittest` module or `pytest`.

7) Resources:
   - SQLalchemy https://www.sqlalchemy.org/
# Installation:
## Installation via Docker-compose:
###1. For the beginning install `docker` and `docker compose` on your machine:
1) [docker](https://docs.docker.com/engine/install/ubuntu/)
2) [docker-compose](https://docs.docker.com/compose/install/)
3) P.S.: Depending on the version use:
    ```commandline
    docker compose
    # or
    docker-compose
    ```

###2. Then git clone this project in your folder.
###3. Go to the folder where are `docker-compose.yml` and `Dockerfile` are located.
###4. Now use following command:
   ```commandline
   docker compose build
   ```
###5. After image building, you can up the containers of one of these commands:
- background mode:
   ```commandline
   docker compose up -d
   ```
- default mode:
   ```commandline
   docker compose up
   ```
###6. If you need to stop the containers:
   ```commandline
    docker compose down
   ```

####Possible errors:
- if you got something like this:
   ```commandline
   Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock:...
   ```

   Use:
   ```commandline
   sudo chmod 666 /var/run/docker.sock
   ```
- if you get `postgres` warnings after app started,
then you should probably change outer port for `postgres` in `docker-compose.yml`:
   ```yaml
   ports:
         - '5432:5432'
  
   # changed to
  
   ports:
         - '5632:5432'
   ```
- if you use ubuntu, then you will probably have a problems with psycopg2.
So install this:
```commandline
sudo apt-get install libpq-dev
```
## Installation via IDE or other:
###1) create env and install packages:
```commandline
pip install pipenv
pipenv shell
pipenv install
```

###2) For start api:
- `Bash`:
   ```bash
   export FLASK_APP=app.py
   flask db init
   flask db migrate
   flask run
   ```
- `Powershell`:
   ```commandline
   $env:FLASK_APP = 'app.py'
   flask db init
   flask db migrate
   flask run
   ```
- `CMD`:
   ```commandline
   set FLASK_APP=app.py
   flask db init
   flask db migrate
   flask run
   ```