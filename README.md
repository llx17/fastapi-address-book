# Address Book API

A minimal FastAPI-based address book application that allows API users to create, update, delete, and retrieve addresses, including searching for addresses within a given distance from a set of coordinates.

---

## Features

- Create an address
- Retrieve an address by ID
- Update an existing address
- Delete an address
- Search for addresses within a given distance
- Validate latitude and longitude inputs
- Store data in SQLite using SQLAlchemy ORM
- Built-in interactive Swagger documentation
- Request logging middleware
- Structured exception handling
- API tests using pytest

---

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Haversine
- Pytest

---

## Project Structure

```text
app/
├── api/         # Route handlers
├── core/        # Config, logging, middleware, exceptions
├── db/          # Database setup
├── models/      # SQLAlchemy ORM models
├── schemas/     # Pydantic request/response schemas
├── services/    # Business logic
└── utils/       # Utility helpers

tests/           # API tests
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd fastapi-address-book
```

### 2. Create and activate virtual environment

#### Windows PowerShell
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

#### Windows CMD
```cmd
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create environment file

Create a `.env` file in the project root with:

```env
APP_NAME=Address Book API
APP_VERSION=1.0.0
DATABASE_URL=sqlite:///./address_book.db
DEBUG=True
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

### 6. Open API docs

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## Running Tests

```bash
pytest
```

---

## API Endpoints

### Health Check
- `GET /health`

### Address CRUD
- `POST /addresses`
- `GET /addresses/{address_id}`
- `PUT /addresses/{address_id}`
- `DELETE /addresses/{address_id}`

### Nearby Search
- `GET /addresses/nearby?latitude=...&longitude=...&distance_km=...`

---

## Example Request

### Create Address

**POST** `/addresses`

```json
{
  "name": "Home",
  "latitude": 10.8505,
  "longitude": 76.2711
}
```

### Nearby Search Example

**GET** `/addresses/nearby?latitude=9.9312&longitude=76.2673&distance_km=100`

---

## Notes

- Coordinates are validated at the API boundary using Pydantic.
- Nearby search is calculated in Python using the `haversine` library.
- SQLite is used for simplicity and portability for this assignment.
- Since SQLite does not provide advanced geospatial querying out of the box, nearby filtering is performed in the service layer.

---