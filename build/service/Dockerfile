# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-slim as requirements

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED=1

# Define temp dir
WORKDIR /temp

# Install poetry
RUN pip install poetry

# Copy poetry config files
COPY ./pyproject.toml /temp/

# Export dependencies in requirements.txt
RUN poetry export -o requirements.txt --without-hashes


# Second layer: installing libraries for building psycopg2
FROM python:3.11-slim as builder

# Install dependencies
RUN apt-get update; \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    libc-dev \
    gcc;


# Third layer (app)
FROM builder

WORKDIR /project

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# For reference app folder as package
ENV PYTHONPATH=/project

# Copy requirements from requirements layer
COPY --from=requirements /temp/requirements.txt /project/requirements.txt

# Install requirements
RUN python3 -m pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /project/app

# Copy project files
COPY ./app .

# Creates a non-root user with an explicit UID and adds permission to access the /marketplace folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /project
USER appuser

# Single handler for cluster node in future * NOW REDECLARED IN COMPOSE *
CMD ["python3", "__main__.py"]
