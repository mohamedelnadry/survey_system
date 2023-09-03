# Employee Survey System

## Introduction
The Employee Survey System is a web application built with Django that allows organizations to conduct surveys amongst employees. Through this platform, HR departments can create, distribute, and analyze surveys with ease.

## Setup and Installation
1. Clone the repository
```bash
git clone git@github.com:mohamedelnadry/survey_system.git
```
2. Change directory
```bash
cd EmployeeSurveySystem
```
3. Setup Environment Variables: Copy `.env.example `to create a `.env` file.

```env
DATABASE_NAME = postgres
DATABASE_USER = postgres
DATABASE_PASSWORD = 1
DATABASE_HOST = db
DATABASE_PORT = 5432
SECRET_KEY = Secret_Key
DEBUG = True
```
4. Install dependencies
```bash
pip install -r requirements.txt
```
5. Run migrations
```bash
python manage.py migrate
```
6. Run the application
```bash
python manage.py runserver
```
7. Open your browser and navigate to `http://127.0.0.1:8000/accounts/registerform`

## End Points and URLs
Below is a list of the available end-points and associated template views:

### Authentication

- Login: `/accounts/login/`
- Logout: `/accounts/logout/`
- Register:`/accounts/registerform/`

### Survey Management

- List Surveys:`/listsurvey/`
- List Submitted Surveys:`/submitedsurvey/`
- Create and Retrieve Question Survey: `/survey/id_survey/`

## API End Points
The system also provides RESTful APIs for programmatic interaction.

### Authentication
- Login API: POST `/accounts/api/token`
```json
{
    "username":"user_name",
    "password":"password"
}
```
- Register API: POST `/accounts/api/register`
```json
{
    "username":"username",
    "password":"password",
    "job_title":"job_title",
    "department":"department"
}
```
### Survey Management
- List All Surveys: GET `/api/survey`
```http
Authorization: Bearer Token
```
- List All Submitted Surveys: GET `/api/submitedsurvey`
```http
Authorization: Bearer Token
```
- Retrieve a Survey: GET `/api/survey/<int:survey_id>/`
```http
Authorization: Bearer Token
```
- Create a Survey: POST `/api/submitsurvey/`
```http
Authorization: Bearer Token
```
```json
{
    "survey": [15],
    "answers": [
        {
            "question_id": 5,
            "rating": 9.00
        },
        {
            "question_id": 8,
            "rating": 12.00
        }
    ]
}
```
