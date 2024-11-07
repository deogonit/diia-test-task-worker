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
  This command starts the services defined under the `cron` profile in detached mode.

- **Stop cron profile**:
  ```bash
  make stop-cron
  ```
  **Equivalent**:
  ```bash
  docker-compose --profile cron down
  ```
  Stops the services associated with the `cron` profile.

- **Start script-only profile**:
  ```bash
  make start-script
  ```
  **Equivalent**:
  ```bash
  docker-compose --profile script-only up -d
  ```
  Starts the services defined under the `script-only` profile in detached mode.

- **Stop script-only profile**:
  ```bash
  make stop-script
  ```
  **Equivalent**:
  ```bash
  docker-compose --profile script-only down
  ```
  Stops the services associated with the `script-only` profile.

### Python Script Command

- **Run the main script**:
  ```bash
  make run
  ```
  **Equivalent**:
  ```bash
  python src/main.py
  ```
  This command runs the Python script located at `src/main.py`.

### Ruff Commands

- **Lint the code**:
  ```bash
  make lint
  ```
  **Equivalent**:
  ```bash
  ruff check src/
  ```
  Runs `ruff` to check for linting issues in the `src` directory.

- **Format the code**:
  ```bash
  make format
  ```
  **Equivalent**:
  ```bash
  ruff format src/
  ```
  Runs `ruff` to format the code in the `src` directory.
