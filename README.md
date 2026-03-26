# Address Book API

A minimal FastAPI-based address book application that allows API users to create, update, delete, and retrieve addresses, including searching for addresses within a given distance from a set of coordinates.

---

## Features

- Secure API endpoints with JSON Web Tokens
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
| Authentication | JWT (PyJWT) |
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
git clone https://github.com/llx17/fastapi-address-book
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

JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

DEMO_USERNAME=demo
DEMO_PASSWORD=demo123
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

### Authentication

| POST | `/auth/login` | Login with username/password to get JWT token |

### Health Check

| GET | `/health` | Health check |

### Address CRUD

| POST | `/addresses` | Create a new address | 
| GET | `/addresses/{address_id}` | Retrieve an address by ID |
| PATCH | `/addresses/{address_id}` | Update an existing address |
| DELETE | `/addresses/{address_id}` | Delete an address |

### Nearby Search

| GET | `/addresses/nearby` | Find addresses within a given distance |

Query parameters: `latitude`, `longitude`, `distance_km`

---

## Example Requests

### Login (Get JWT Token)

```bash
POST /auth/login
Content-Type: application/json

{
  "username": "demo",
  "password": "demo123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

### Create Address

With JWT token in Authorization header:

```bash
POST /addresses
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Home",
  "latitude": 10.8505,
  "longitude": 76.2711
}
```

### Using curl with Bearer Token

```bash
curl -X GET "http://localhost:8000/addresses/nearby?latitude=10.0&longitude=76.0&distance_km=100" \
  -H "Authorization: Bearer {access_token}"
```

### Nearby Search

```json
GET /addresses/nearby?latitude=9.9312&longitude=76.2673&distance_km=100
Authorization: Bearer {access_token}
```

---

## Authentication

All address endpoints require JWT authentication. Here's the authentication flow:

1. **Login** - POST `/auth/login` with demo username and password
2. **Get Token** - Receive JWT access token with 24-hour expiration
3. **Use Token** - Include token in `Authorization: Bearer {token}` header for protected endpoints
4. **Token Expires** - When token expires, login again to get a new token

### Demo Credentials
- **Username:** `demo`
- **Password:** `demo123`

---

## Notes

- All address endpoints are protected with JWT authentication. Use the `/auth/login` endpoint to obtain a token.
- Coordinates are validated at the API boundary using Pydantic.
- Nearby search distance is calculated using the `haversine` library.
- SQLite is used for simplicity and portability.
- Since SQLite does not support advanced geospatial queries, distance filtering is handled in the service layer.
- Docker support is included for consistent execution across environments.
- JWT tokens expire after 24 hours (configurable via `JWT_EXPIRATION_HOURS`).

---