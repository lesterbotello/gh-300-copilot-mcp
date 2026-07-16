# Mergington High School Activities API

A FastAPI application that allows students to view and sign up for extracurricular activities with persistent SQLite storage.

## Features

- View all available extracurricular activities
- Sign up for activities
- Persist data across restarts using SQLite
- Manage schema with Alembic migrations

## Getting Started

1. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Run the application:

   ```
   uvicorn src.app:app --reload
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Remove a student from an activity                                |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

3. **Registrations** - Links students to activities and persists enrollment state.
4. **Complaints and feedback** - Placeholder tables for the later role-based workflow.

All operational data is stored in SQLite, so it survives restarts. Use Alembic for schema changes:

```
alembic upgrade head
```
