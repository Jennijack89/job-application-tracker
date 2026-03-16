# Job Application Tracker
IT Senior Capstone - Job application Tracking &amp; Progress System

## Project Overview
This application helps job seekers keep track of their job applications, update statuses, and view summaries of their activity. Users can create an account, log in, and manage all job applications in one place.

## Tech Stack
- **Backend:** Python (Flask framework)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (or another relational database)
- **Version Control:** GitHub
- **Development Environment:** Replit/VS code

## Key Features
- Create and log into a secure user account
- Add, update, and view job applications
- Track application statuses and waiting times
- View weekly summaries of job search activity

## Features Implmented

- [] Feature #1: 
- [] Feature #2:
- [] Feature #3:
- [] Feature #4:
- [] Feature #5:
- [] Feature #6:

## Running the Application
- Do steps in order, and you will only need to do steps 2 and 4 one-time.
- Note: if you add any new Python packages, run: pip freeze > requirements.txt , and it   will update the required things we all need. 
- Once you create the /venv folder, create a .gitignore file and add the following text

Python virtual environment
venv/
__pycache__/
*.pyc

### 1. Navigate to the project folder
cd path\to\job-application-tracker

### 2. Create your own virtual environment (one-time)
python -m venv venv
Note:*** Create a virtual environment (Everyone will have their own folder-do not add your /venv folder to the repo)


### 3. Activate the virtual environment (every-time you want enter the environment)
.\venv\Scripts\Activate

### 4. Install all required packages (one-time)
pip install -r requirements.txt

### 5. Run the Flask app
py app.py  #Windows
python app.py
python3 app.py #macOS/Linux

### 6. Open your web browser and go to:
http://localhost:5000

### 7. Deactivate the virtual environment when done:
Terminal type: deactivate

## Important Merge Update 3/15/26

-Merged user registration code and application tracking code into one main Flask app: app.py

-Combined database usage so the app now uses one shared database: database/app.db

-Kept the users table in app.db for account creation data

-Added/used the applications table in app.db for job application tracking

-Moved application data from database/jobs.db into database/app.db

-Updated merged routes so dashboard/add/edit/delete application features now run from app.py

-Updated route redirects from old index references to dashboard

-Removed old unused files:

    -honey_app.py

    -database/jobs.db

    -merge_jobs_into_app.py

    -templates/index.html

-Verified working features:

    -Create account

    -Save user to database

    -Dashboard display

    -Add application

    -Delete application

