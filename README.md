# money-tracker
A Django project based on Django Rest Framework with CBV (views,generic,viewset)

## Overview of Project Components and Information Flow
This [Miro Diagram](/diagrams/miro.jpg) provides an overview of how all components of the project work together and how information flows between the client, API server, and database.



## User Authentication and Transaction Flows
The [User Authentication Flow](/diagrams/user-authentication(version1).png) covers the sign-up and sign-in processes, ensuring users can register and sign in using OAuth 2.0 tokens. The [Transaction Flow](/diagrams/transaction(version2).png) includes creating, updating, and retrieving transactions.

## Features

- **CRUD for Transactions**
- **CRUD for Profile**

## Prerequisites

- Python 3.x
- Pytest
- PostgreSQL
- pgAdmin4
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

6. **How to Access pgAdmin**
    
    Make sure you don't have `pgAdmin4` installed on your local machine. If it's installed, make sure pgAdmin4 on your local machine runs on a different port than the pgAdmin4 service in Docker.

    1. Open pgAdmin4 in your browser at http://127.0.0.1:5050.
    2. Click on Add New Server.
    3. In the General tab, enter a name for the server (e.g., PostgreSQL).
    4. Go to the Connection tab and set:
        - Host: db (this is the service name defined in docker-compose.yml).
        - Port: 5432.
        - Username: from your db service environment.
        - Password: from your db service environment.
    5. Save and Connect.

7. **How to Use redis:**

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

8. **How to Run Tests:**

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

9. **How to Use RabbitMQ:**

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

10. **Configuration:**
    
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

    ```bash
    DJANGO_SECRET_KEY='your_secret_key'
    DJANGO_DEBUG=True
    DJANGO_ALLOWED_HOSTS='localhost, 127.0.0.1'
    REDIS_URL='redis://localhost:6379/1'
    ```

## Rate Limiting Middleware
This middleware implements rate limiting for both authenticated and public API calls in a Django application

### Key Features

**Rate Limiting:** Enforces limits on the number of API calls based on user authentication status.

**Public Routes**  Defines specific public routes that have their own rate limits. 
- /api/v2/signin
- /api/v2/signup
- /admin

**Rate Limits:**
- Authenticated Users: 10 API calls per minute.
- Unauthenticated Users and Public Routes: 5 API calls per minute.

**Token Authentication** Utilizes token-based authentication to identify users and apply rate limits accordingly. In Django, middlewares execute before view-level authentication (such as DRF’s token authentication), so request.user might not be populated yet

### Usage
Install Middleware: Add the RateLimitMiddleware to your Django settings.
    
```bash
MIDDLEWARE = [
    ...
    'core.middleware.RateLimitMiddleware',
    ...
]
```

### How It Works:
- The middleware checks the request path to determine if it's a public route or requires authentication.
- For public routes, it applies the RATE_LIMIT_PUBLIC limit.
- For authenticated users, it applies the RATE_LIMIT_AUTHENTICATED limit.
- If the rate limit is exceeded, a `429 Too Many Requests` response is returned.

### Example Response

```json
{
    "detail": "Rate limit exceeded. Try again later."
}

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
- [x] Change the database to PostgreSQL.
- [x] Rate Limiter
- [x] RabbitMQ




