# Join-Backend
Backend Applicaton for Join

# Description
This is a backend project developed with Django 5.2 and Django REST Framework. It provides an API for managing tasks and projects, including functionalities to create, update, delete, and retrieve tasks and subtasks.

## Technologies
- Django: 5.2
- Django REST Framework: For API development  
- SQLite: Standard database (can be configured)  

## Installation

### Requirements
Make sure you have Python 3.13 or higher and pip installed.

1. Clone the repository:  
   `git clone https://github.com/dampolo/joinfrontend.git`

2. Create and activate a virtual environment with the following commands:  
   `"env/Scripts/activate" or env/Scripts/activate`  
   `source env/bin/activate   # On Windows: env\Scriptsctivate`

   You should see on the left, next to path (env)

3. Install the dependencies:  
   `pip install -r requirements.txt`

4. Configure the database:  
   Run the migrations to initialize the database:  
   `python manage.py migrate`

5. Start the development server:  
   `python manage.py runserver`

## API Endpoints

### Authentication
- `POST /auth/registration/`: Register a user  
- `POST /auth/login/`: Log in a user  

### Task Management
- `GET /api/tasks/`: Retrieve all tasks  
- `POST /api/tasks/`: Create a new task  
- `PATCH /api/tasks/<int:id>/`: Update a specific task  
- `DELETE /api/tasks/<int:id>/`: Delete a specific task  

### User/Contact Management
- `GET /api/users/`: Retrieve all tasks  
- `POST /api/users/`: Create a new task  
- `PATCH /api/users/<int:id>/`: Update a specific task  
- `DELETE /api/users/<int:id>/`: Delete a specific task 

## Troubleshooting
If you encounter issues, check the following:

- Ensure that the database is correctly configured and migrations have been run.
- Verify the `requirements.txt` for the correct dependency versions.

## Contributors
Damian Poloczek
