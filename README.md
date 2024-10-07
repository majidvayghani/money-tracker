# money-tracker
A Django project based on Django Rest Framework with CBV (views,generic,viewset)

## Features

- **CRUD for Transactions**

## Getting Started

### Prerequisites

- Python 3.x
- Docker (To Do)
- Git

### Installation

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
## Linting and Code Style
I have written a simple linter file. In this file, the `CodeStyleChecker` class checks three simple rules to ensure they are followed in my code. The `visit_FunctionDef()` method checks rules 1 and 2, while the `visit_ClassDef()` method checks rule 3. For simplicity, you can specify which files the linter should analyze at the beginning.

**Rule 1:** Function names should contain only lowercase letters and be longer than 2 characters.

**Rule 2:** Functions used in view files for APIs should have names that are at least two parts, separated by underscores, and must include HTTP verbs in their names.

**Rule 3:** Class names must start with an uppercase letter.

### How to run the linter
Simply execute the `run_linter.py` file, which is a Python script. This script will run on all files within the project folder that are listed in the 'TARGET_FILES' list. If any files do not adhere to the rules, the details will be 'log_filename', and finally, the log will be printed as output.

## API Endpoints

The following table summarizes the available API endpoints for managing transactions.

| **Method** | **Endpoint**                | **Description**                         |
|------------|-----------------------------|-----------------------------------------|
| POST       | `/api/v1/transactions/`     | Create a new transaction                |
| GET        | `/api/v1/transactions/`     | Retrieve all transactions               |
| GET        | `/api/v1/transactions/{id}/` | Retrieve a specific transaction by ID   |
| PUT        | `/api/v1/transactions/{id}/` | Update an existing transaction          |
| DELETE     | `/api/v1/transactions/{id}/` | Delete a transaction                    |

The following table summarizes the available API endpoints for registration.

| **Method** | **Endpoint**                | **Description**                         |
|------------|-----------------------------|-----------------------------------------|
| POST       | `/api/v1/auth/register/`     | Create a new user                |
| POST        | `/api/v1/auth/signin/`       | signin                            |



## Here are simple curl commands for GET and POST requests:

### Get All Transactions

```bash
curl -X GET http://localhost:8000/api/v1/transactions/ -H "Content-Type: application/json"
```

### Create a New Transaction

```bash
curl -X POST http://localhost:8000/api/v1/transactions/ \
-H "Content-Type: application/json" \
-d '{
  "amount": 50.0,
  "category": "Personal",
  "description": "Internet",
  "tag": "Internet"
}'
```

## To Do
- [ ] Modify the signIn API code to perform a single database query for all checks.
- [ ] Generate HTML version of swagger api doc `redocly build-docs my-swagger.yml -o docs.html`
- [ ] How to run unit tests and integration tests