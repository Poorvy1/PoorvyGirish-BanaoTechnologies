
# Mini Hospital Management System (HMS)

## Project Overview
A Mini Hospital Management System that allows doctors to manage their availability and patients to book appointments.  
The system also sends email notifications using a serverless AWS Lambda function.

## Features
- Doctor and Patient authentication
- Role-based access control
- Doctor availability management
- Patient appointment booking
- Double-booking prevention using database transactions
- Serverless email notifications (Signup & Booking)

## Tech Stack
- Backend: Django
- Database: SQLite (can be replaced with PostgreSQL)
- Email Service: AWS Lambda (Serverless Framework – local)
- Language: Python



## How to Run

### 1. Run Backend (Django)
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## 2. Run email server
Run email-service
cd email-service
npm install -g serverless
npm install serverless-offline
serverless offline



