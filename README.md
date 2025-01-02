# Project Management API (CRUD)

This project is a simple API built with Django that allows management of users, projects, tasks, and comments. It supports CRUD operations for these entities and is intended to be consumed by front-end applications or other services.

Here is a detailed database schema,
![tyechforing schema](https://github.com/user-attachments/assets/a8b4deee-1e98-415d-9d89-a5714f09a246)


## Features

- **Users**
  - Register User
  - Login User (Authentication using token)
  - Get User Details
  - Update User Details
  - Delete User

- **Projects**
  - List Projects
  - Create Project
  - Retrieve Project Details
  - Update Project Details
  - Delete Project

- **Tasks**
  - List Tasks in a Project
  - Create Task in a Project
  - Retrieve Task Details
  - Update Task Details
  - Delete Task

- **Comments**
  - List Comments on a Task
  - Create Comment on a Task
  - Retrieve Comment Details
  - Update Comment Details
  - Delete Comment

## Setup Instructions

### 1. Clone the repository

To get started, clone the repository to your local machine:

```bash
git clone https://github.com/mujjasaikumar/projectManagement_API.git
```

```bash
cd projectManagement_API
```

## 2. Install Dependencies

Create a virtual environment and install the required dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use .venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Apply Migrations

Run the migrations to set up your database:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. Run the Development Server

Start the server with:

```bash
python manage.py runserver
```

The API will now be accessible at http://localhost:8000.


API Endpoints
-------------

### 1. Users

#### Register User

-   **URL:** `/api/users/register/`
-   **Method:** `POST`
-   **Body:**

    

    `{
      "username": "newuser",
      "email": "user@example.com",
      "password": "password123",
      "first_name": "John",
      "last_name": "Doe"
    }`

#### Login User

-   **URL:** `/api/users/login/`
-   **Method:** `POST`
-   **Body:**

    

    `{
      "username": "newuser",
      "password": "password123"
    }`

#### Get User Details

-   **URL:** `/api/users/{id}/`
-   **Method:** `GET`

#### Update User

-   **URL:** `/api/users/{id}/`
-   **Method:** `PUT/PATCH`
-   **Body:**

    

    `{
      "first_name": "Jane",
      "last_name": "Smith"
    }`

#### Delete User

-   **URL:** `/api/users/{id}/`
-   **Method:** `DELETE`

### 2. Projects

#### List Projects

-   **URL:** `/api/projects/`
-   **Method:** `GET`

#### Create Project

-   **URL:** `/api/projects/`
-   **Method:** `POST`
-   **Body:**

    

    `{
      "name": "New Project",
      "description": "A project description",
      "owner": 1
    }`

#### Retrieve Project

-   **URL:** `/api/projects/{id}/`
-   **Method:** `GET`

#### Update Project

-   **URL:** `/api/projects/{id}/`
-   **Method:** `PUT/PATCH`
-   **Body:**

    

    `{
      "name": "Updated Project Name",
      "description": "Updated project description"
    }`

#### Delete Project

-   **URL:** `/api/projects/{id}/`
-   **Method:** `DELETE`

### 3. Tasks

#### List Tasks in Project

-   **URL:** `/api/projects/{project_id}/tasks/`
-   **Method:** `GET`

#### Create Task in Project

-   **URL:** `/api/projects/{project_id}/tasks/`
-   **Method:** `POST`
-   **Body:**

    

    `{
      "title": "New Task",
      "description": "Task description",
      "status": "To Do",
      "priority": "Medium",
      "assigned_to": 1,
      "due_date": "2025-01-01T00:00:00"
    }`

#### Retrieve Task Details

-   **URL:** `/api/tasks/{id}/`
-   **Method:** `GET`

#### Update Task

-   **URL:** `/api/tasks/{id}/`
-   **Method:** `PUT/PATCH`
-   **Body:**

    

    `{
      "status": "In Progress",
      "priority": "High"
    }`

#### Delete Task

-   **URL:** `/api/tasks/{id}/`
-   **Method:** `DELETE`

### 4. Comments

#### List Comments on a Task

-   **URL:** `/api/tasks/{task_id}/comments/`
-   **Method:** `GET`

#### Create Comment on Task

-   **URL:** `/api/tasks/{task_id}/comments/`
-   **Method:** `POST`
-   **Body:**

    

    `{
      "text": "This is a comment",
      "author": 1
    }`

#### Retrieve Comment

-   **URL:** `/api/comments/{id}/`
-   **Method:** `GET`

#### Update Comment

-   **URL:** `/api/comments/{id}/`
-   **Method:** `PUT/PATCH`
-   **Body:**

    

    `{
      "text": "Updated comment text"
    }`

#### Delete Comment

-   **URL:** `/api/comments/{id}/`
-   **Method:** `DELETE`

---
Please find the detailed Swagger API documentation here, http://127.0.0.1:8000/swagger/
