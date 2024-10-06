# DataDynamo Back-End System

**Customer Company:** DataDynamo Technologies

## Project Description

DataDynamo Technologies is a data-driven startup focused on developing scalable and efficient back-end solutions for data processing and analysis. This project implements a scalable back-end system for DataDynamo’s data analytics platform, capable of processing large volumes of data efficiently, performing complex analytical tasks, and managing datasets asynchronously.

The back-end is built with Django, Celery for task management, Redis as the message broker, and PostgreSQL as the database. The system is containerized using Docker, ensuring portability and scalability.

## Features

- **CRUD Operations**: Support for creating, reading, updating, and deleting datasets and data analysis tasks.
- **Asynchronous Task Processing**: Data processing tasks are managed asynchronously using Celery and Redis.
- **PostgreSQL Database**: Relational database support for efficient storage and retrieval of data.
- **Dockerized Deployment**: Ensures scalable and portable deployments.
- **RESTful API**: Interact with the system using a fully documented REST API.

## Architecture

The architecture of this system includes:
- **Django** as the web framework for handling API requests.
- **Celery** for managing background tasks (data processing).
- **Redis** as a message broker for Celery.
- **PostgreSQL** for database management.
- **Docker** for containerization.

### Components

1. **Django**: Manages HTTP requests and provides the API layer.
2. **Celery**: Handles asynchronous task execution (data processing).
3. **Redis**: Acts as the message broker between Django and Celery.
4. **PostgreSQL**: Stores data about datasets and analysis tasks.

## Installation and Setup

### Prerequisites

- **Python 3.x**
- **Docker and Docker Compose**
- **PostgreSQL**

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/datadynamo-backend.git
cd datadynamo-backend
```

### Step 2: Set Up Environment Variables
Create a .env file in the project’s root directory with the following content:

```
POSTGRES_DB=datadynamo_db
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
```
These environment variables are used by Docker to configure the PostgreSQL database.

### Step 3: Build and Run with Docker
Run the following command to build and start all services (Django, Celery, Redis, PostgreSQL) using Docker Compose:
```
docker-compose up --build
```
This command will:

    1. Build Docker images for Django and Celery.
    2. Start Redis, PostgreSQL, Django, and Celery in separate containers.

### Step 4: Migrate the Database
Once the services are running, open a new terminal window and run the following command to apply database migrations:
```
docker-compose exec web python manage.py migrate
```
### Step 5: Create a Superuser (Optional)
You can create a Django superuser to access the Django admin panel:

```
docker-compose exec web python manage.py createsuperuser
```
### Step 6: Access the Application
    1. API Endpoints: Access the API at http://localhost:8000/api/.
    2. Admin Panel: If you created a superuser, you can access the Django admin panel at http://localhost:8000/admin/.
    3. Celery: The Celery worker will automatically process tasks in the background.

## API Endpoints
Here are the main API endpoints available in this project:

### Datasets
    - GET /api/datasets/: Retrieve all datasets.
    - POST /api/datasets/: Create a new dataset.
    - GET /api/datasets/{id}/: Retrieve a specific dataset by ID.
    - PUT /api/datasets/{id}/: Update a dataset by ID.
    - DELETE /api/datasets/{id}/: Delete a dataset by ID.
### Data Analysis Tasks
    - GET /api/tasks/: Retrieve all data analysis tasks.
    - POST /api/datasets/{id}/process/: Trigger a data analysis task for a specific dataset.
    - GET /api/tasks/{id}/: Retrieve a specific task by ID and view its status and result.

### Task Processing
    - Celery is used to handle the background processing of large datasets. When a dataset is submitted for analysis, the task is sent to Celery for processing, allowing the API to remain responsive.
    - Redis acts as the message broker, managing communication between Django and Celery.

## Example API Workflow
    1. Upload a Dataset:
        Send a POST request to /api/datasets/ with dataset details.

    2. Trigger Data Processing:
        After the dataset is created, send a POST request to /api/datasets/{id}/process/ to start processing the data.

    3. Check Task Status:
        Use a GET request to /api/tasks/{id}/ to check the status of the data analysis task.

### Docker Compose Setup
The docker-compose.yml file orchestrates the services (Django, Celery, Redis, PostgreSQL):

```
version: '3'

services:
  db:
    image: postgres
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  celery:
    build: .
    command: celery -A datadynamo worker --loglevel=info
    volumes:
      - .:/app
    depends_on:
      - redis
```

## Celery Task Example
The background task for data processing is handled by Celery and is defined in analytics/tasks.py:

```
from celery import shared_task
from .models import DataAnalysisTask

@shared_task
def process_data_task(task_id):
    task = DataAnalysisTask.objects.get(id=task_id)
    task.start_task()

    # Simulate data processing (replace with real logic)
    result = f"Data processed for dataset {task.dataset.name}"

    task.complete_task(result)
```
