# money-tracker
A Django project based on Django Rest Framework with CBV (views,generic,viewset)

## Features

- **CRUD for Transactions a

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
    python3 manage.py migrate
    ```

# API Endpoints

The following table summarizes the available API endpoints for managing transactions.

| **Method** | **Endpoint**                | **Description**                         |
|------------|-----------------------------|-----------------------------------------|
| POST       | `/api/v1/transactions/`     | Create a new transaction                |
| GET        | `/api/v1/transactions/`     | Retrieve all transactions               |
| GET        | `/api/v1/transactions/{id}/` | Retrieve a specific transaction by ID   |
| PUT        | `/api/v1/transactions/{id}/` | Update an existing transaction          |
| DELETE     | `/api/v1/transactions/{id}/` | Delete a transaction                    |

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