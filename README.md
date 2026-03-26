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
- Request logging middleware
- Structured exception handling
- API tests using pytest
- Docker support for easy setup and execution

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite |
| Validation | Pydantic |
| Distance | Haversine |
| Testing | Pytest |
| Deployment | Docker |

---

## Project Structure

```
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

You can run the application in two ways:

- **Local** (Python)
- **Docker** (recommended for reviewers)

---

### Option 1: Run Locally (Python)

#### 1. Clone the repository

```bash
git clone
cd fastapi-address-book
```

#### 2. Create and activate virtual environment

**Windows PowerShell**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows CMD**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Create environment file

Create a `.env` file in the project root:

```env
APP_NAME=Address Book API
APP_VERSION=1.0.0
DATABASE_URL=sqlite:///./address_book.db
DEBUG=True

```

#### 5. Run the application

```bash
uvicorn app.main:app --reload
```

### Option 2: Run with Docker (Recommended)

#### 1. Build Docker image

```bash
docker build -t fastapi-address-book .
```

#### 2. Run container

**Windows PowerShell**
```powershell
docker run --name fastapi-address-book -p 8000:8000 --env-file .env -v ${PWD}:/app fastapi-address-book
```

**Windows CMD**
```cmd
docker run --name fastapi-address-book -p 8000:8000 --env-file .env -v %cd%:/app fastapi-address-book
```

**Mac/Linux**
```bash
docker run --name fastapi-address-book -p 8000:8000 --env-file .env -v $(pwd):/app fastapi-address-book
```

#### 3. Stop container

```bash
docker stop fastapi-address-book
```

#### 4. Remove container

```bash
docker rm -f fastapi-address-book
```

---

## Running Tests

```bash
pytest
```

---

## API Endpoints

### Health Check

| Method | Endpoint |
|---|---|
| GET | `/health` |

### Address CRUD

| Method | Endpoint | Description |
|---|---|---|
| POST | `/addresses` | Create a new address |
| GET | `/addresses/{address_id}` | Retrieve an address by ID |
| PUT | `/addresses/{address_id}` | Update an existing address |
| DELETE | `/addresses/{address_id}` | Delete an address |

### Nearby Search

| Method | Endpoint | Description |
|---|---|---|
| GET | `/addresses/nearby` | Find addresses within a given distance |

Query parameters: `latitude`, `longitude`, `distance_km`

---

## Example Requests

### Create Address

```json
POST /addresses
{
  "name": "Home",
  "latitude": 10.8505,
  "longitude": 76.2711
}
```

### Nearby Search

```
GET /addresses/nearby?latitude=9.9312&longitude=76.2673&distance_km=100
```

---

## Notes

- Coordinates are validated at the API boundary using Pydantic.
- Nearby search distance is calculated using the `haversine` library.
- SQLite is used for simplicity and portability.
- Since SQLite does not support advanced geospatial queries, distance filtering is handled in the service layer.
- Docker support is included for consistent execution across environments.

---