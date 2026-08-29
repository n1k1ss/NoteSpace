# NoteSpace 📝

A modern and responsive note-taking web application built with **FastAPI and JavaScript**.

NoteSpace is a project for learning and implementing real-world backend concepts such as REST APIs, data validation, authentication, and database integration.

## ✨ Features

* Create notes through a REST API
* View created notes
* Get individual notes by ID
* Responsive interface for desktop, tablet, and mobile
* Pydantic data validation
* JavaScript `fetch()` API requests
* Static file serving with FastAPI
* JWT authentication *(in development)*
* PostgreSQL integration *(planned)*

## 🛠 Tech Stack

### Backend

* Python
* FastAPI
* Pydantic
* JWT

### Frontend

* HTML5
* CSS3
* JavaScript

### Database

* PostgreSQL *(planned)*

## 📁 Project Structure

```text
NoteSpace/
├── main.py
├── main.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── script.js
│
├── .gitignore
└── README.md
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
pip install fastapi uvicorn pydantic
```

### 4. Start the server

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 🔌 API

### Create a note

```http
POST /api/notes
```

Request body:

```json
{
    "title": "Python",
    "text": "Learning FastAPI"
}
```

### Get all notes

```http
GET /api/notes
```

### Get a specific note

```http
GET /api/notes/{index}
```

## 🔐 Authentication

Authentication using **JWT tokens** is currently being developed.

The planned authentication flow:

```text
Register
   ↓
Login
   ↓
JWT token
   ↓
Authenticated request
   ↓
User's notes
```

Each user will eventually be able to access only their own notes.

## 🗺 Roadmap

* [x] FastAPI backend
* [x] REST API
* [x] Note creation
* [x] Note retrieval
* [x] Responsive frontend
* [x] Static files
* [ ] User registration
* [ ] JWT authentication
* [ ] User-specific notes
* [ ] PostgreSQL database
* [ ] Update notes
* [ ] Delete notes
* [ ] Production deployment

## 📚 Purpose

NoteSpace is primarily a learning project focused on understanding how a modern web application works from frontend to backend.

The project demonstrates the connection between:

```text
HTML / CSS
     ↓
JavaScript
     ↓
REST API
     ↓
FastAPI
     ↓
PostgreSQL
```

## 📄 License

This project is currently for educational purposes.