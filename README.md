# Zywa Card Status Update

This project aims to provide a solution for updating the status of cards based on data from CSV files provided by partner companies. The system tracks the status of cards from pickup to delivery, including any exceptions and returns. The project is implemented using Django for the backend, Celery for task management and background process, and Django REST framework for API development.

![image](https://github.com/EGhost98/Zywa-card-status/assets/76267623/7fcac6ca-aa1f-4ab6-b11d-19f7b3f60ada)


## Table of Contents 

- [Docker-compose Setup](#docker-compose-setup)
- [Virtual Enviroment Setup](#virtual-enviroment-setup)
- [Steps to Setup Celery locally to Ingest Asynchronously](#steps-to-setup-celery-locally-to-ingest-asynchronously)
- [Approach](#approach)
- [Tech Stack](#tech-stack)
- [Possible Improvements](#possible-improvements)
- [Architectural Decisions](#architectural-decisions)
- [API Reference](#api-reference)

## Setup

Instructions for setting up the project locally and using Virtual Enviroment and Docker-Compose, and also how to setup Celery Worker.

### Docker-Compose Setup

**Requirements**
    - Docker
    - Docker-Compose

To Run The Project Follow These Steps - 

1. Clone the repository: `git clone <repository_url>`.
2. Move into the Project Directory: `cd Zywa-card-status`.
3. Ensure Docker is Running.
4. Build Docker Image  `docker-compose build`.
5. Run the Container in detached mode `docker-compose up -d`. (Wait for around 10s after container Spins up and then acces the Provided [EndPoints](#api-reference) )
6. To Ingest data Asynchronously open Docker Exec and navigate to app/backend and execute `python manange.py ingest-data-async`, or use the provided enpoints in `localhost/swagger`.
7. Access the Swagger Interactive API DOCS at `localhost/swagger`.
8. Stop the Container with `docker-compose down`.

***Access Admin Dashboard:*** Access the Swagger Interactive API DOCS at `localhost/admin` and login credentials username - `admin` , password - `admin` to browse the models or delete existing one for testing purposes. 

### Virtual Enviroment Setup

**Requirements**:
   - Python (3.6+)
   - Pip
   - Virtualenv

To run the project, follow these steps:

1. Clone the repository: `git clone <repository_url>`
2. Create a Virtual Python Environment `python -m venv env`.
3. Activate the Virtual Environment (if using Git-Bash) `source env/Scripts/Activate`
4. Navigate to the project directory: `cd Zywa-card-status`
5. Install the dependencies: `pip install -r requirements.txt` -> `cd backend`.
6. Create a .env and copy contents of .env.example and configure accordingly. (local or Your Own Database or the provide one).
7. Run the migrate command `python manage.py migrate`.
8. Run the custom Command `py manage.py ingest-data`. (To Populate the DB with CSV Files Located in Backend/card_status/card-data)
9. Another Method to Get Data from CSV is through using Celery Asynchronous Tasks, useful when dataset is large. (To Do this Follow [These](#steps-to-setup-celery-locally-to-ingest-asynchronously) Steps)
10. Run the application: `python manage.py runserver`.
11. Access the Swagger Open-API Documentation of API's at : `http://localhost:8000/swagger/`


### Steps to Setup Celery locally to Ingest Asynchronously

1. Complete the [Virtual Enviroment Setup](#virtual-enviroment-setup) Above. 
2. To Start Celery Worker Process Locally, we need to have a running instance of redis Database which will act as Message Broker for Celery Worker.
3. Install redis from [here](https://redis.io/docs/install/install-redis/).
4. Start redis Server on port 6379 (Default Port).
5. Open a terminal in `backend` directory.
6. Start Celery Worker Process by ```celery -A core worker --pool=solo -l info```.
7. Open Another terminal and run Custom `Manage.py` command `py manage.py ingest-data-async` or visit Swagger Doc and Hit the POST Request on Refresh Commands to Ingest Data from Respective CSV.

##### Custom Django Management Command

- `py manage.py ingest-data`: This command Ingest data into database with data from four CSV files: "pickup", "delivery_exceptions", "delivered", and "returned". It uses Celery tasks to process each file and update the database.

- `py manage.py ingest-data-async` : This command also ingests data into the database using the data from our CSV files. This function performs the ingestion process asynchronously, leveraging Celery to handle the tasks.

## Project Structure

```bash
project/
├── backend/
│   ├── card_status/
│   │   ├── migrations/
│   │   ├── card-data/
│   │   │    └── *.csv
│   │   ├── management/
│   │   │   └──commands
│   │   │       ├──ingest-data-async.py
│   │   │       └──ingest-data.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   └── views.py
│   ├── core/
│   │   ├── settings.py
│   │   ├── celery.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── static/
│   └── manage.py
│── requirements.txt
│── docker-compose.yml
└── docker/
    ├── backend/
    │   ├── Dockerfile
    │   ├── server-entrypoint.sh
    │   └── worker-entrypoint.sh
    └── nginx/
         └── default.conf

```

## Approach

- **Django Model**: A `CardStatus` model is used to store the status of each card, along with its ID, user mobile, and timestamp. This model is updated based on the data from CSV files.

- **Celery Tasks**: Celery tasks are used to update the `CardStatus` model from the data in the CSV files. Separate tasks are defined for each type of CSV file (Delivered, Delivery Exceptions, Pickup, Returned).

- **CSV Parsing**: CSV parsing is used to maintain a consistent data format. The user mobile numbers are formatted to get the last 9 digits, and datetime objects are used to compare timestamps for updating the model.

- **Custom Django `Manage.py` Commands**: Custom Django `manage.py` commands are utilized for ingesting data into the database. Both synchronous and asynchronous approaches are implemented to handle data ingestion efficiently.

- **Docker-Compose**: Docker-compose is used to run a multi-container system, effectively integrating Celery, Redis, and PostgreSQL without needing to set them up individually. This simplifies the deployment process and ensures that the application runs consistently in different environments.

- **Manual POST Endpoints**: Manual POST endpoints are provided to trigger data ingestion from .csv files manually. This feature allows for flexibility in managing data updates and integrates seamlessly with the existing system architecture.

## Tech Stack

- **Python**: Python is chosen for its simplicity and readability. It provides a rich ecosystem of libraries for CSV parsing, datetime manipulation, and task management.

- **Django**: Django is used for its built-in ORM, which simplifies database operations. It also provides a robust framework for building web applications, including REST APIs. Django comes bundled with security features such as protection against SQL injection, and cross-site request forgery (CSRF).Django Also Provides a Built-in Admin Dashboard. Django can be deployed easily as a microservice on serverless architecture, allowing for efficient scaling and resource management.

- **Celery**: Celery is used for asynchronous task processing, to handle large datasets, and can also be used for handling updates based on changes in the CSV files or can be scheduled using `celery-beat`.

- **Docker**: Docker is used for containerization, enabling easy deployment and scaling of the application. It provides a consistent environment for the application to run, ensuring that it behaves the same way across different environments.

- **Nginx**: Nginx is used as a reverse proxy server to handle client requests and distribute them to the appropriate backend servers.


## Architectural Decisions

- **Database**: PostgreSQL is chosen as the database backend for its reliability and scalability.

- **API**: Django REST framework is used for building the API, which provides a flexible and powerful toolkit for web APIs.

- **Deployment**: The system is deployed using Docker containers for easy deployment and scalability. Docker Compose is used to manage the multi-container setup, including Django, Celery, Redis,PostgreSQL, and Nginx.

## Possible Improvements

- **Logging**: Enhanced logging can help in debugging and monitoring the system.

- **Optimization**: The code can be optimized for performance, especially for large datasets.

- **File Watcher**: Implementing a file watcher, such as Watchdog, can be added to watch files and update the database periodically based on changes in the CSV files.

- **Consistent Data Stream**: Specify a consistent data stream to ingest data into the system continuously, ensuring that updates are processed in real-time.

## API Reference

#### Get Card Status

```http
  GET /get-card-status/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `card_id` | `string` | Card ID for whose status is requested |
| `user_mobile`| `string` | User's Contact Number Whoose Card Status is Requested|

#### Update Delivered Data
```bash
  POST refresh/delivered
```
- **Description:** Update card status data from Delivered CSV source using Celery Worker.

#### Update Delivery Exceptions Data
```bash
  POST refresh/delivery-exceptions
```
- **Description:** Update card status data from Delivery Exceptions CSV source using Celery Worker.

#### Update Pickup Data
```bash
  POST refresh/pickup
```
- **Description:** Update card status data from Pickup CSV source using Celery Worker.

#### Update Returned Data
```bash
  `POST refresh/returned`
```
- **Description:** Update card status data from Returned CSV source using Celery Worker.