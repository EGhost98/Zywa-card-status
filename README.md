# Zywa Card Status Update

This project aims to provide a solution for updating the status of cards based on data from CSV files provided by partner companies. The system tracks the status of cards from pickup to delivery, including any exceptions and returns. The project is implemented using Django for the backend, Celery for task management and background process, and Django REST framework for API development.


## Table of Contents 

- [Setup](#setup)
- [How to run the Tests](#how-to-run-the-tests)
- [Reason for choice of Tech Stack](#reason-for-choice-of-tech-stack)
- [API Documentation](#api-documentation)
- [Search Functionality](#search-functionality)
- [Rate Limiting](#rate-limiting)

## Setup

Instructions for setting up the project locally and using Virtual Enviroment and Docker-Compose.

### Virtual Enviroment Setup - 

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
6. Create a .env and copy contents of .env.example and configure accordingly. (local or Your Own Database).
7. Run the migrate command `python manage.py migrate`.
8. Run the custom Command `py manage.py merge_data`. (To Populate the DB with CSV Files Located in Backend/card_status/card-data)
9. Another Method to Get Data from CSV is through using Celery Asynchronous Tasks, useful when dataset is large. (To Do this Follow These Steps)
10. Run the application: `python manage.py runserver`.
11. Access the Swagger Open-API Documentation of API's at : `http://localhost:8000/swagger/`


## Custom Django Management Command Explanation - `py manage.py merge_data`

This command populates the database with data from four CSV files: "pickup", "delivery_exceptions", "delivered", and "returned". It uses Celery tasks to process each file and update the database. After processing, it outputs a success message.

## Approach

- **Django Model**: A `CardStatus` model is used to store the status of each card, along with its ID, user mobile, and timestamp. This model is updated based on the data from CSV files.

- **Celery Tasks**: Celery tasks are used to update the `CardStatus` model based on changes in the CSV files. Separate tasks are defined for each type of CSV file (Delivered, Delivery Exceptions, Pickup, Returned).

- **CSV Parsing**: The CSV files are parsed using the `csv` module in Python. Each row of the CSV file is processed to extract relevant information and update the `CardStatus` model accordingly.

## Language and Framework

- **Python**: Python is chosen for its simplicity and readability. It provides a rich ecosystem of libraries for CSV parsing, datetime manipulation, and task management.

- **Django**: Django is used for its built-in ORM, which simplifies database operations. It also provides a robust framework for building web applications, including REST APIs. Django comes bundled with security features such as protection against SQL injection, cross-site scripting (XSS), cross-site request forgery (CSRF), and clickjacking. Django can be deployed easily as a microservice on serverless architecture, allowing for efficient scaling and resource management.

- **Celery**: Celery is used for asynchronous task processing, which is essential for handling updates based on changes in the CSV files.

## Possible Improvements

- **Error Handling**: Improved error handling could be implemented to handle cases where CSV data is incorrect or missing.

- **Logging**: Enhanced logging can help in debugging and monitoring the system.

- **Optimization**: The code can be optimized for performance, especially for large datasets.

- **Testing**: Comprehensive testing, including unit tests and integration tests, can ensure the reliability of the system.

- **User Interface**: A user interface can be developed to visualize the status of cards and provide an admin interface for managing the system, though Djnago Admin Dashboard Works here too.

## Architectural Decisions

- **Database**: PostgreSQL is chosen as the database backend for its reliability and scalability.

- **API**: Django REST framework is used for building the API, which provides a flexible and powerful toolkit for web APIs.

- **Deployment**: The system can be deployed using Docker containers for easy deployment and scalability.
