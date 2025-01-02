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

4. **Install Snyk CLI:**
    ```bash
    curl https://static.snyk.io/cli/latest/snyk-linux -o snyk
    chmod +x ./snyk
    mv ./snyk /usr/local/bin/ 
    ```

5. **Apply migrations:**
    ```bash
    python3 manage.py makemigrations
    
    python3 manage.py migrate
    ```

6. **Start Docker:**
    
    Make sure you have `Docker` installed. You can install it from [docs.docker.com/engine/instal](https://docs.docker.com/engine/install/):
    ```bash
    docker compose up
    ```
    After running docker compose up, make sure the containers are running.

7. **How to Access pgAdmin**
    
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

8. **How to Use redis:**

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

9. **How to Run Tests:**

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

10. **How to Use RabbitMQ:**

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

11. **Configuration:**
    
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

## ELK Stack Configuration for Logging and Monitoring
The ELK Stack (Elasticsearch, Logstash, and Kibana) is used to collect, process, and visualize log data.

The logging system in this project is configured to capture important events, errors, and debug information for better monitoring and debugging. Logs are generated for key actions, including user registration, sign-in, and other critical events.

### Log Handlers
Logs are directed to the console and a log file. The console handler displays log messages in the terminal during development, while the file handler stores them in ``app_name.log`` for future reference.

### Architecture

**1.** Elasticsearch: Stores and indexes log data.

**2.** Logstash: Processes and forwards log data to Elasticsearch.

**3.** Kibana: Visualizes the log data stored in Elasticsearch.

### Users in ELK Stack
``kibana_system User:``

 - The ``kibana_system`` user is a predefined service account required for Kibana's internal operations.

- It allows Kibana to:

    - Authenticate with Elasticsearch.

    - Perform backend tasks such as reading and writing to the .kibana index.

- Why Define in Docker Compose?

    - Kibana needs this user to start and function correctly.

    - Since it is only used for internal communication, it is best defined during setup and not manually later.
**Note:** This user cannot log in to Kibana and is strictly for system communication.

``Admin User:``

- To access Kibana's interface, you need a user with administrative privileges (e.g., ``superuser``).

- Steps to create an admin user are provided in the "Configuration" section.

- Why Not Define a superuser in Docker Compose?

    - A superuser is required for administrative access to Kibana, but defining it in Docker Compose is less secure because sensitive credentials would be hardcoded in configuration files.

### Configuration

Add the following variables to your `.env` file:

```ini
# file paths
APP_LOG_PATH = your_path

# ElK credentials
ELASTIC_PASSWORD=your_elastic_password
KIBANA_PASSWORD=your_kibana_password
```

### Key Features
**lasticsearch:** Runs on http://127.0.0.1:9200.

**Kibana:** Accessible at http://127.0.0.1:5601.

**Logstash:** Listens on http://127.0.0.1:5044 for logs. ( if in logstash.conf defined TCP inpt)

### Running the ELK Stack
```
docker compose up -d
```

### Adding a Kibana's Superuser Manually:

Access the Elasticsearch Container:
```bash
docker exec -it elasticsearch bash
```

Create a Superuser:
```bash
elasticsearch-users useradd <username> -p <password> -r superuser
```

**Note:** Use this credentials for log in to Kibana.

## Linting and Code Style
I have written a simple linter file. In this file, the `CodeStyleChecker` class checks three simple rules to ensure they are followed in my code. The `visit_FunctionDef()` method checks rules 1 and 2, while the `visit_ClassDef()` method checks rule 3. For simplicity, you can specify which files the linter should analyze at the beginning.

**Rule 1:** Function names should contain only lowercase letters and be longer than 2 characters.

**Rule 2:** Functions used in view files for APIs should have names that are at least two parts, separated by underscores, and must include HTTP verbs in their names.

**Rule 3:** Class names must start with an uppercase letter.

### How to run the linter
Simply execute the `run_linter.py` file, which is a Python script. This script will run on all files within the project folder that are listed in the 'TARGET_FILES' list. If any files do not adhere to the rules, the details will be 'log_filename', and finally, the log will be printed as output.

## Security Vulnerability Scanning with Snyk
This project uses [Snyk](https://snyk.io/) to help identify and fix security vulnerabilities in dependencies, containers, and infrastructure code.

### Steps to Use Snyk:
**1. Sign up and Log in to Snyk's website:**

**2. Run the Following Command:** 
After signing up or logging in, run the command below to authenticate your Snyk CLI.
```bash
snyk auth
```
**Note:** You can also use the command without signing up or logging in first. However, you'll need to open the Snyk dashboard in a new browser window to complete the process.

**3. Install Snyk CLI:** 
```bash
curl https://static.snyk.io/cli/latest/snyk-linux -o snyk
chmod +x ./snyk
mv ./snyk /usr/local/bin/ 
```
### Scan for security issues
Navigate into your code’s directory: cd ~/projects/my-project/
Refer to the instructions that follow on specific content types: open-source packages, source code, containers and IaC (Infrastructure as Code).

**1. open-source packages**

To scan your open-source packages for vulnerabilities ensure all dependencies are installed or there is a supported lockfile. Then, run:
```bash
snyk monitor
```
```snyk monitor``` Creates projects in your Snyk account to be continuously monitored for open-source vulnerabilities and license issues. View the latest snapshots and scan results in the Web UI, on the Projects page.

**2. snyk code test**

To scan your source code for vulnerabilities, ensure Snyk Code is enabled in Settings > Snyk Code. Then run:
```bash
snyk code test
```

```snyk code test``` Scans your source code for vulnerabilities introduced by your first party code.

**3. Containers**

To scan container images for vulnerabilities copy the command below and specify the container image by replacing <repository> and <tag>:
```bash
snyk container monitor <repository>:<tag>
```
```snyk container test``` Scans your container images for any known vulnerabilities.

```snyk container monitor``` Captures the container image layers and dependencies and monitor for vulnerabilities. View the latest snapshots and scan results in the Web UI, on the Projects page.

### Fixing Vulnerabilities
Snyk provides an easy way to fix vulnerabilities automatically by upgrading the affected dependencies:
```bash
snyk fix
```
The ```snyk fix``` command is a powerful feature in the Snyk CLI that helps automatically resolve vulnerabilities in your project's dependencies. It modifies dependency management files (e.g., package.json for Node.js or requirements.txt for Python) to replace vulnerable packages with secure versions.

**Note:** Backup Before Execution: Since this command makes changes to dependency files, it’s recommended to create a backup of your project before running it.

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
- [x] Set Up Logging
- [ ] Health Check Configuration (Use packages like django-health-check to monitor the database, message broker (RabbitMQ), and file system.)
- [ ] Add Basic Monitoring Tools
    - Implement basic metrics using the django-prometheus package
    - Track request counts, response statuses, and request processing times
- [ ] Log Analysis (Forward logs to tools like the ELK Stack or simpler tools like Graylog for analysis.)
