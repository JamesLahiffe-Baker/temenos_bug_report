# Bug Tracker Web Application

A FastAPI-based bug tracking system for managing website issues. This app allows users to register and report bugs, and provides admin users with management features such as updating bug statuses and user privileges.

------------------------------------------------------------------------------

## Features

- User registration and login
- Admin role auto-assignment to first user
- Bug reporting with title, description, priority, and associated website
- Bug comment section (admin/user)
- Bug filtering and sorting
- Admin user management: promote or delete users
- Role-based dashboard interface
- SQLite database (for local testing)

------------------------------------------------------------------------------

## Project Structure

```
.
├── controllers/          #Route handlers split by feature
├── database.py           #DB engine setup and Base model
├── main.py               #FastAPI app and router registration
├── models.py             #SQLAlchemy models
├── templates/            #Jinja2 HTML templates
├── static/               #Static assets (CSS, images)
├── requirements.txt      #Python dependencies
└── README.md             #This file
```

------------------------------------------------------------------------------

## Database Schema

### Entity Relationships

```
\[User] 1---\* \[BugReport] *---1 \[Website]
\[BugReport] 1---* \[BugComment] \*---1 \[User]
```

### Tables

- **Users**
  - `user_id` (PK)
  - `username`
  - `email`
  - `hashed_password`
  - `role` (user/admin)
  - `created_at`

- **Websites**
  - `website_id` (PK)
  - `name`
  - `url`

- **BugReports**
  - `bug_id` (PK)
  - `title`
  - `description`
  - `status` (Open, In Progress, Resolved)
  - `priority` (Low, Medium, High)
  - `reported_at`
  - `website_id` (FK to Website)
  - `reported_by_user_id` (FK to User)
  - `assigned_admin_id` (FK to User, nullable)

- **BugComments**
  - `comment_id` (PK)
  - `bug_id` (FK to BugReport)
  - `comment`
  - `created_at`
  - `created_by_user_id` (FK to User)

------------------------------------------------------------------------------

## Dependencies

This project relies on the following Python packages, listed in `requirements.txt`. They are essential for the FastAPI application, database operations, form handling, authentication, and rendering templates.

Install them using:

```bash
pip install -r requirements.txt
```

| Package            | Purpose                                                                 |
| ------------------ | ----------------------------------------------------------------------- |
| `fastapi`          | Web framework for building APIs with Python                             |
| `uvicorn`          | ASGI server to run FastAPI applications                                 |
| `jinja2`           | Template engine for rendering HTML pages                                |
| `sqlalchemy`       | ORM for database interactions                                           |
| `python-multipart` | Enables form data parsing for file uploads and forms                    |
| `bcrypt`           | Password hashing utility used by `passlib`                              |
| `python-jose`      | Handling JWT (JSON Web Tokens) for secure session logic                 |
| `passlib[bcrypt]`  | Secure password hashing via `CryptContext` used in authentication logic |

------------------------------------------------------------------------------

## How to Run This App Locally

### 1. Clone the Repository

```bash
git clone https://github.com/JamesLahiffe-Baker/temenos_bug_report.git
cd temenos_bug_report
```

### 2. Install Dependencies

Make sure you are in a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  #On Windows: venv\\Scripts\\activate
```

Then install the requirements:

```bash
pip install -r requirements.txt
```

### 3. Initialise the Database

This will create `app.db` using SQLite and the necessary tables:

```bash
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 4. Start the FastAPI Server

```bash
uvicorn main:app --reload
```

By default, the app will be accessible at:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

------------------------------------------------------------------------------

## Deployment (e.g. Render)

To deploy, ensure you include the following:

* `requirements.txt`
* `start` command like:

  ```
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```
* Include `controllers/`, `templates/` and `static/` directories
* Replace SQLite with a production-grade DB (e.g. PostgreSQL) if needs be
* No environment variables for secrets and configs needed, but can be added

------------------------------------------------------------------------------

## Admin Role

* The **first user** to register is automatically assigned the **admin** role.
* Admins can:

    * Update bug status and priority
    * Promote or delete users
    * View all bugs across all websites

------------------------------------------------------------------------------

## Notes

* This app uses in-memory session storage (`sessions = {}`), which is **not suitable for production**.
* For production, use secure storage, HTTPS, and proper session or token handling.
* Use `.env` and config files to manage sensitive data and DB credentials.

------------------------------------------------------------------------------

## License

MIT License — 2025 

------------------------------------------------------------------------------
