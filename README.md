# Tasks2Do

<p align="center">
  <strong>A lightweight task management web application built with Flask.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.1.3-black?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0.50-red?logo=sqlalchemy" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap" alt="Bootstrap">
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite" alt="SQLite">
</p>

---

## Overview

**Tasks2Do** is a personal task management web application built with Flask.

The application provides a simple workflow for creating, organizing, and tracking tasks. Users can create an account, manage their own tasks, assign categories and deadlines, filter and sort their task list, and mark tasks as completed.

The project focuses on implementing the core pieces of a small full-stack web application while keeping the codebase relatively lightweight.

---
## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Main Components](#main-components)
- [Security & Validation](#security--validation)
- [Getting Started](#getting-started)
- [Project Scope](#project-scope)
- [About](#about)

---

## Features

| | Feature | Description |
|:---:|---|---|
| 👤 | **Authentication** | Register and log in with a personal account |
| 🔐 | **Password Security** | Passwords are stored using secure hashing |
| ➕ | **Create Tasks** | Add titles, descriptions, categories, and optional deadlines |
| ✏️ | **Edit Tasks** | Update incomplete tasks |
| 🗑️ | **Delete Tasks** | Remove tasks from your list |
| ✅ | **Complete Tasks** | Mark tasks as completed |
| ⏳ | **Deadlines** | Set deadlines and track the remaining time |
| 🏷️ | **Categories** | Organize tasks using custom categories |
| 🔎 | **Filtering** | Filter by category, creation date, deadline, or status |
| ↕️ | **Sorting** | Sort tasks by date or deadline |
| 📄 | **Pagination** | Navigate through tasks page by page |
| 📱 | **Responsive UI** | Adapt the interface to different screen sizes |
| 📝 | **Rich Text** | Create formatted descriptions using CKEditor |

---

## Tech Stack

### Backend

<p>
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.1.3-black?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0.50-red?logo=sqlalchemy" alt="SQLAlchemy">
</p>

- **Python**
- **Flask**
- **Flask-SQLAlchemy**
- **Flask-Login**
- **Flask-WTF**
- **Flask-CKEditor**

### Frontend

<p>
  <img src="https://img.shields.io/badge/HTML5-orange?logo=html5" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-blue?logo=css3" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-yellow?logo=javascript" alt="JavaScript">
  <img src="https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap" alt="Bootstrap">
</p>

- HTML
- CSS
- JavaScript
- Bootstrap 5
- Jinja2 Templates
- CKEditor

### Database

<p>
  <img src="https://img.shields.io/badge/SQLite-003B57?logo=sqlite" alt="SQLite">
</p>

- **SQLite**
- **SQLAlchemy ORM**

---

## Project Structure

```text
tasks2do/
│
├── instance/
│   └── task_manager.db
│
├── static/
│   ├── css/
│   │   ├── bootstrap.min.css
│   │   └── style.css
│   │
│   └── js/
│       └── bootstrap.bundle.min.js
│
├── templates/
│   ├── add_task.html
│   ├── base.html
│   ├── home_page.html
│   ├── login.html
│   ├── register.html
│   └── show_tasks.html
│
├── app.py
├── forms.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Main Components

| File / Directory | Responsibility |
|---|---|
| [`app.py`](./app.py) | Application routes, database models, authentication, and task operations |
| [`forms.py`](./forms.py) | Registration, login, and task forms with validation |
| [`templates/`](./templates/) | Jinja2 HTML templates and application interface |
| [`static/css/`](./static/css/) | Bootstrap and custom CSS |
| [`static/js/`](./static/js/) | Frontend JavaScript functionality |
| [`requirements.txt`](./requirements.txt) | Python dependencies |
| [`instance/`](./instance/) | Local SQLite database |

---

## Security & Validation

The application includes several basic security and validation mechanisms:

- Password hashing using **Werkzeug**
- CSRF protection through **Flask-WTF**
- User authentication with **Flask-Login**
- User-specific task access
- Password structure validation
- Username and password whitespace validation
- Completed tasks cannot be edited
- Deadlines cannot be set in the past

Each task is associated with the user who created it, so task operations are restricted to the corresponding user.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/EHMoeini/tasks2do.git
cd tasks2do
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Flask secret key

The application reads its secret key from the `FLASK_KEY` environment variable.

#### Windows PowerShell

```powershell
$env:FLASK_KEY="your-secret-key"
```

#### macOS / Linux

```bash
export FLASK_KEY="your-secret-key"
```

If `DB_URI` is not provided, the application uses SQLite:

```text
sqlite:///task_manager.db
```

### 5. Run the application

```bash
python app.py
```

Then open the local Flask address in your browser.

---

## Project Scope

Tasks2Do focuses on the core functionality of a **personal task management system**.

The current implementation covers:

```text
User
 │
 ├── Register / Login
 │
 ▼
Task Manager
 │
 ├── Create & Edit
 ├── Categories
 ├── Deadlines
 ├── Filter & Sort
 └── Pagination
 │
 ▼
Complete / Delete
```

The project intentionally keeps the architecture relatively simple and focuses on the fundamentals of building a small web application with Flask, a relational database, server-side validation, authentication, and interactive frontend behavior.

---


## About

Tasks2Do was developed as a practical Flask project to explore the development of a complete task-management workflow.

The project brings together:

**Authentication · Database Persistence · Form Validation · CRUD Operations · Filtering · Sorting · Pagination · Frontend Interaction**

while keeping the overall application small enough to understand and work with comfortably.

---

<p align="center">
  Built with Python & Flask
</p>
