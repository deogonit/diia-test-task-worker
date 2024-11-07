# Project README

## Test task for Diia Company
This project, called `diia-test-task-worker`, is test project for the position of Python engineer. The main purpose of this project is to gather data from the Internet and save it in database

## Prerequisites
Ensure that you have the following installed:
- **Docker** and **Docker Compose**
- **Python** (version 3.12 is recommended)
- **uv** (for Python package and environment management)

## Local Development
- Install dependencies using **uv**
  ```bash
  uv sync
  ```
  Or you can install dependencies using commands:
  ```
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```
- Run a main Python script:
  ```
  python src/main.py
  ```

### Docker Compose Commands

- **Start cron profile**:
  ```bash
  make start-cron
  ```
  **Equivalent**:
  ```bash
  docker-compose --profile cron up -d
  ```
  This command starts database and the demon services which pull and save data every minute. According to the terms of the task, the data should be updated every quarter, but in order to speed up the testing, it was decided to update the data every minute. The results of the worker you can see in file logs/cron.log

- **Stop cron profile**:
  ```bash
  make stop-cron
  ```
  **Equivalent**:
  ```bash
  docker-compose --profile cron down
  ```

- **Start script-only profile**:
  ```bash
  make start-script
  ```
  **Equivalent**:
  ```bash
  docker-compose --profile script-only up -d
  ```
  This command starts database and only the worker, which will exit after executino. The logs you can see using docker or docker-compose utillity.

- **Stop script-only profile**:
  ```bash
  make stop-script
  ```
  **Equivalent**:
  ```bash
  docker-compose --profile script-only down
  ```

### Python Script Command

- **Run the main script**:
  ```bash
  make run
  ```
  **Equivalent**:
  ```bash
  python src/main.py
  ```

### Ruff Commands

- **Lint the code**:
  ```bash
  make lint
  ```
  **Equivalent**:
  ```bash
  ruff check src/
  ```

- **Format the code**:
  ```bash
  make format
  ```
  **Equivalent**:
  ```bash
  ruff format src/
  ```
