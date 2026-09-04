# NoteSpace 📝

A note-taking web application built with **FastAPI**, **SQLAlchemy (async)**, and vanilla **JavaScript**.

NoteSpace is a learning project for practicing real-world backend concepts: REST APIs, cookie-based session authentication, password hashing, async ORM usage, and database migrations.

## ✨ Features

* User registration and login
* Cookie-based session authentication (no JWT — sessions are stored in the database)
* Password hashing with **Argon2** (via `pwdlib`)
* Create notes tied to the authenticated user
* Retrieve all of a user's notes, or a single note by ID
* Access control — a user can only read their own notes (`403` otherwise)
* Async SQLAlchemy + PostgreSQL
* Database schema versioning with Alembic
* Static file serving and simple multi-page frontend (login / register / notes)

## 🛠 Tech Stack

### Backend
* Python 3.13
* FastAPI
* SQLAlchemy 2.0 (async, via `asyncpg`)
* Alembic (migrations)
* Pydantic / `pydantic-settings`
* `pwdlib[argon2]` for password hashing

### Frontend
* HTML5
* CSS3
* Vanilla JavaScript (`fetch()`)

### Database
* PostgreSQL

## 📁 Project Structure

```text
NoteSpace/
├── main.py                        # FastAPI app entrypoint, page routes
├── requirements.txt
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/                  # migration scripts
│
├── app/
│   ├── index.html                 # notes page
│   ├── login.html
│   ├── register.html
│   │
│   ├── api/
│   │   ├── auth.py                # /api/auth/register, /api/auth/login
│   │   └── notes.py               # /api/notes/create, /api/notes/check[/{id}]
│   │
│   ├── core/
│   │   └── config.py              # settings (reads .env)
│   │
│   ├── db/
│   │   ├── database.py            # async engine & session maker
│   │   ├── dependencies.py        # get_db dependency
│   │   └── models/                # User, Note, Session ORM models
│   │
│   ├── schemas/                   # Pydantic request models
│   │
│   └── security/
│       ├── passwords.py           # hash_password / verify_password
│       ├── sessions.py            # session token creation
│       └── dependencies.py        # get_current_user / get_optional_user
│
├── static/
│   ├── css/
│   └── js/
│
├── .env.example
└── .gitignore
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/n1k1ss/NoteSpace.git
cd NoteSpace
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows**
```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

Copy the example env file and fill in your PostgreSQL connection string:

```bash
cp .env.example .env
```

```env
DATABASE_URL=postgresql+asyncpg://username:password@host:port/database
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the server

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

Interactive API docs (Swagger UI):

```text
http://127.0.0.1:8000/docs
```

## 🔌 API

All authenticated endpoints rely on an HTTP-only `session_token` cookie set at login/register — there is no `Authorization` header / bearer token to pass manually.

### Auth

**Register**
```http
POST /api/auth/register
```
```json
{
    "username": "nik",
    "email": "nik@example.com",
    "password": "your-password"
}
```
Creates the user, opens a session, sets the `session_token` cookie.

**Login**
```http
POST /api/auth/login
```
```json
{
    "email": "nik@example.com",
    "password": "your-password"
}
```
Verifies credentials, opens a new session, sets the `session_token` cookie.

### Notes

*(all require a valid session cookie)*

**Create a note**
```http
POST /api/notes/create
```
```json
{
    "title": "Python",
    "text": "Learning FastAPI"
}
```

**Get all of my notes**
```http
GET /api/notes/check
```

**Get a specific note by ID**
```http
GET /api/notes/check/{id}
```
Returns `403 Forbidden` if the note doesn't belong to the current user.

## 🔐 Authentication

Authentication is **session-based**, not JWT:

```text
Register or Login
       ↓
Server creates a Session row (token + expiry) in the database
       ↓
Token is sent back as an HTTP-only cookie
       ↓
Every request → session_token cookie is looked up in the DB
       ↓
Valid & not expired → request proceeds as that user
```

Sessions expire after 30 days. Expired sessions are deleted from the database on next use.

## 🗺 Roadmap

* [x] FastAPI backend
* [x] REST API
* [x] Note creation
* [x] Note retrieval (all + by ID)
* [x] Responsive frontend
* [x] Static files
* [x] User registration
* [x] Session-based authentication
* [x] User-specific notes (with access control)
* [x] PostgreSQL database
* [x] Alembic migrations
* [ ] Update notes
* [ ] Delete notes
* [ ] User avatar upload
* [ ] Logout endpoint
* [ ] Production deployment

## 📚 Purpose

NoteSpace is primarily a learning project focused on understanding how a modern web application works from frontend to backend:

```text
HTML / CSS
     ↓
JavaScript (fetch)
     ↓
FastAPI (REST API + cookie sessions)
     ↓
SQLAlchemy (async)
     ↓
PostgreSQL
```

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.