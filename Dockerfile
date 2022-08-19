# set args
ARG PYTHON_VERSION=3.10
ARG PYTHON_VERSION_SUFFIX=slim-buster

# pull python image from docker hub
FROM python:${PYTHON_VERSION}-${PYTHON_VERSION_SUFFIX} AS builder

# set env values
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# update pip and install pipenv
RUN pip install --no-cache-dir --upgrade \
    pip \
    pipenv

# create tmp folder
WORKDIR /usr/src/tmp

# copy pipenv files to tmp folder
COPY Pipfile.lock /usr/src/tmp/

# convert Pipfile.lock to requirements.txt
# and install all dependencies by pip
RUN pipenv requirements > requirements.txt && \
    pip install --no-cache-dir --target=/usr/src/dependencies \
    -r requirements.txt

FROM python:${PYTHON_VERSION}-${PYTHON_VERSION_SUFFIX}

# copy all dependencies into container
COPY --from=builder /usr/src/dependencies /usr/src/dependencies

# instal gunicorn for production server
RUN pip install --no-cache-dir gunicorn

# create backend folder
WORKDIR /usr/src/backend

# copy api to container
COPY . /usr/src/backend

# add dependencies path to env
ENV PYTHONPATH=${PYTHONPATH}:"/usr/src/dependencies"

# remove unnecessary files
RUN rm Pipfile
RUN rm Pipfile.lock
RUN rm -d -r nginx/