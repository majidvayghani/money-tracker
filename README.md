# money-tracker
A Django project based on Django Rest Framework with CBV (views,generic,viewset)

## Features

- **CRUD for Transactions**
- **CRUD for Profile**

## Prerequisites

- Python 3.x
- Pytest
- Redis
- RabbitMQ
- Docker
- Git

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/majidvayghani/money-tracker.git
   cd money-tracker
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```bash
    python3 manage.py makemigrations
    
    python3 manage.py migrate
    ```

5. **Start Docker:**
    
    Make sure you have `Docker` installed. You can install it from [docs.docker.com/engine/instal](https://docs.docker.com/engine/install/):
    ```bash
    docker compose up
    ```
    After running docker compose up, make sure the containers are running.

6. **How to Use redis:**

    Make sure you don't have `Redis` installed on your local machine. If it's installed, make sure Redis on your local machine runs on a different port than the Redis service in Docker.

    1. Open RedisInsight in your browser at http://127.0.0.1:5540.
    2. Click Add Redis Database.
    3. Enter the following details:
        - Database Alias: Any name (e.g., "Local Redis").
        - Host: redis (this is the service name in Docker Compose).
        - Port: 6379.
        - Password: Leave blank if you haven't set a password.
    4. Click Add Redis Database.
    5. Select the database and choose db1 (this is the database number specified in the Redis configuration settings)

7. **How to Run Tests:**

    ```bash
    export DJANGO_SETTINGS_MODULE=your_project.settings.development
    ```

    To run all tests in the project, navigate to the project root directory and execute:
    ```bash
    pytest
    ```

    To run only the unit tests, use the following command:
    ```bash
    pytest -m "unit"
    ```

    To run only the integration tests, use this command:
    ```bash
    pytest -m "integration"
    ```

8. **How to Use RabbitMQ:**

    Ensure RabbitMQ is running in your Docker setup. RabbitMQ should be configured in `docker compose.yml` file.

    The RabbitMQ setup for this project uses two main functionalities:
    1. **Email Notification**: Sends a welcome email after a user signs up.
    2. **Logging**: Logs the user's signup event to a file.
        
    #### Queues and Exchanges:

    - **`signup_queue`**: This queue is used to send signup email notifications.
    - **`logs` exchange**: A fanout exchange used for logging the user signups. The exchange broadcasts the log messages to multiple consumers.

    The application declares a durable queue (`signup_queue`) and an exchange of type `fanout` for broadcasting log messages.

    #### Consumers:

    - **`Email Consumer`**: Listens to signup_queue and sends a welcome email to users after they sign up.
    - **`Log Consumer`**: Logs user signup events by consuming messages from the logs exchange.

    #### Running the Consumers:
    ```bash
    python consumers.py
    ```

    #### Managing the RabbitMQ Server:
    You can monitor RabbitMQ queues and exchanges using the RabbitMQ Management UI if it's enabled. Access the UI by visiting:
    ```bash
    http://localhost:15672
    ```
    - Default username: guest
    - Default password: guest

9. **Configuration:**
    
    Project follows a modular settings structure to manage different environments. The settings are divided into the following files:

    - **settings.py**: Contains the base settings shared across all environments.
    - **development.py**: Includes settings specific to the development environment, such as debug options and local databases.
    - **production.py**: Holds settings for the production environment, optimized for security and performance.

    ```bash
    export DJANGO_SETTINGS_MODULE=my_project.settings.development #For development
    export DJANGO_SETTINGS_MODULE=my_project.settings.production #For production
    ```
    To manage sensitive information and environment-specific settings, Create a `.env` file in the root directory of your project and add the necessary environment variables.(it is included in the `.gitignore`).
    
    Here’s an example:

    ```env
    DJANGO_SECRET_KEY='your_secret_key'
    DJANGO_DEBUG=True
    DJANGO_ALLOWED_HOSTS='localhost, 127.0.0.1'
    REDIS_URL='redis://localhost:6379/1'
    ```
## Linting and Code Style
I have written a simple linter file. In this file, the `CodeStyleChecker` class checks three simple rules to ensure they are followed in my code. The `visit_FunctionDef()` method checks rules 1 and 2, while the `visit_ClassDef()` method checks rule 3. For simplicity, you can specify which files the linter should analyze at the beginning.

**Rule 1:** Function names should contain only lowercase letters and be longer than 2 characters.

**Rule 2:** Functions used in view files for APIs should have names that are at least two parts, separated by underscores, and must include HTTP verbs in their names.

**Rule 3:** Class names must start with an uppercase letter.

### How to run the linter
Simply execute the `run_linter.py` file, which is a Python script. This script will run on all files within the project folder that are listed in the 'TARGET_FILES' list. If any files do not adhere to the rules, the details will be 'log_filename', and finally, the log will be printed as output.

## API Endpoints

The table below summarizes some of the available API endpoints for managing transactions and users.

| **Method** | **Endpoint**                | **Description**                         |
|------------|-----------------------------|-----------------------------------------|
| POST       | `/api/v2/transactions/`     | Create a new transaction                |
| GET        | `/api/v2/transactions/{id}/` | Retrieve a specific transaction by ID   |
| PUT        | `/api/v2/transactions/{id}/` | Update an existing transaction          |
| DELETE     | `/api/v2/transactions/{id}/` | Delete a transaction                    |

| **Method** | **Endpoint**                | **Description**                         |
|------------|-----------------------------|-----------------------------------------|
| POST       | `/api/v2/signup`      | Create a new user                |
| POST       | `/api/v2/signin`      | signin                            |
| POST       | `/api/v2/signout`     | signout                          |
| GET/PUT/DELETE       | `/api/v2/user`        | Retrieve, update(email&password) and delete a user                            |
| GET/PUT/DELETE       | `/api/v2/profile`      | Retrieve, update and delete a profile

## Here are simple curl commands for GET and POST requests:

### Logout
```bash
curl --location --request POST '127.0.0.1:8000/api/v2/signout' \
--header 'Authorization: Token <token>>'
```

### Update the Profile

```bash
curl --location --request PUT 'http://127.0.0.1:8000/api/v2/profile' \
--header 'Authorization: Token <token>' \
--header 'Content-Type: application/json' \
--data '{
"first_name": "first_name",
"last_name": "last_name"
}'
```

### Get All Transactions
```bash
curl -X GET http://localhost:8000/api/v2/transactions/ -H "Content-Type: application/json"
```

### Create a New Transaction
```bash
curl -X POST http://localhost:8000/api/v2/transactions/ \
-H "Content-Type: application/json" \
-d '{
  "amount": 50.0,
  "category": "Personal",
  "description": "Internet",
  "tag": "Internet"
}'
```

## To Do
- [ ] Update linter: remove extra spaces and ...
- [ ] Implement permissions to manage user access
- [ ] Write more unit tests for the models, views and other components
- [ ] Write additional integration tests for further evaluation of the project
- [ ] Generate HTML version of swagger api doc: `redocly build-docs my-swagger.yml -o docs.html`
- [ ] Update Swagger for the new routes
- [x] How to run unit tests and integration tests
- [ ] Finish the project logic and check for possible errors. Also, write suitable responses.
- [ ] Change the database to PostgreSQL.
- [ ] Rate Limiter
- [ ] RabbitMQ




