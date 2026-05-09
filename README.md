# Job Application Tracker
## IT Senior Capstone - Job Application Tracking & Progress System

---

# Project Overview

The Job Application Tracker is a web application designed to help job seekers organize and manage their job applications in one place. Users can create accounts, log in securely, add job applications, update application statuses, and monitor their progress throughout the hiring process.

This application was created to solve the problem of managing multiple job applications manually through spreadsheets or notes. The system provides a centralized dashboard that helps users stay organized and track their job search activity more efficiently.

---

# Team Members

- Honey Patel – Dashboard UI, application tracking, validation, status updates, login functionality, user account features
- Jennifer – Sprint planning, GitHub management, project organization, backend support, and application features
- Tyree – Helped with login page implementation and frontend support
- Zion – Helped with sprint planning and project coordination

---

# Tech Stack

## Backend
- Python
- Flask Framework

## Frontend
- HTML
- CSS
- Bootstrap
- JavaScript

## Database
- SQLite

## Version Control
- GitHub

## Development Environment
- VS Code
- Replit

---

# Key Features

- Create and log into a secure user account
- Add, update, edit, and delete job applications
- Track application statuses and waiting times
- View weekly summaries of job search activity
- Dashboard summary cards with application statistics
- Form validation and error handling
- Shared SQLite database integration
- Redirect and navigation improvements

---

# Features Implemented

- [x] User registration and account creation
- [x] User login and authentication system
- [x] Add, edit, and delete job applications
- [x] Dashboard summary cards and statistics
- [x] Application status tracking and waiting time display
- [x] Weekly application activity summaries
- [x] Form validation and error handling
- [x] Shared SQLite database integration
- [x] Redirect and navigation improvements
- [x] GitHub collaboration and sprint issue tracking

---

# Project Objectives Assessment

## Objective 1: Implement secure user account creation and login
**Status:** Met

**Explanation:** We successfully implemented user registration and login functionality using Flask and SQLite. User information is securely stored in the database, and validation was added for required fields and password matching.

---

## Objective 2: Create a job application tracking system
**Status:** Met

**Explanation:** Users can add, edit, update, and delete job applications. The system stores company name, job title, application status, location, and application date inside the shared SQLite database.

---

## Objective 3: Build a dashboard with summary statistics
**Status:** Met

**Explanation:** The dashboard displays summary cards showing total applications, interviews, offers, rejected applications, and weekly application activity. Data is dynamically retrieved from the database.

---

## Objective 4: Implement status tracking and progress monitoring
**Status:** Met

**Explanation:** Users can update application statuses such as Applied, Interview, Offer, and Rejected. Waiting time tracking and progress summaries were also added to improve organization.

---

## Objective 5: Use GitHub for collaboration and sprint management
**Status:** Met

**Explanation:** GitHub was used throughout development for version control, sprint issue tracking, collaboration, and merging team contributions into the main application.

---

# Installation Instructions

## Prerequisites

Make sure the following are installed:

- Python 3.x
- Git
- VS Code or another code editor

---

## Step 1: Clone the Repository

</>bash
git clone <repository-url>
```

---

## Step 2: Navigate to the Project Folder

</>bash
git clone <repository-url>

git clone https://github.com/jennijack89/job-application-tracker.git

## Step 3: Create a Virtual Environment (One-Time Setup)

</>bash
python -m venv venv
```

Each team member should create their own virtual environment.  
Do NOT upload the `venv` folder to GitHub.

---

## Step 4: Activate the Virtual Environment

### Windows

</>bash
.\venv\Scripts\Activate
```

### macOS/Linux

</>bash
source venv/bin/activate
```

---

## Step 5: Install Required Packages

</>bash
pip install -r requirements.txt
```

If new packages are added later, update requirements using:

</>bash
pip freeze > requirements.txt
```

---

## Step 6: Run the Flask Application

### Windows

</>bash
py app.py
```

OR

</>bash
python app.py
```

### macOS/Linux

</>bash
python3 app.py
```

---

## Step 7: Open the Application

Open your browser and go to:

```text
http://localhost:5002
```

---

## Step 8: Deactivate the Virtual Environment

</>bash
deactivate
```

---

# Usage Instructions

1. Create a user account using the registration page
2. Log into the application
3. Add job applications with company details and status
4. Edit or delete applications when needed
5. Monitor application statuses and waiting times
6. View dashboard summaries and weekly statistics

---

# Important Merge Update – 3/15/26

- Merged user registration code and application tracking code into one main Flask app: `app.py`
- Combined database usage into one shared database: `database/app.db`
- Kept the users table in `app.db` for account creation data
- Added and updated the applications table for job application tracking
- Moved application data from `database/jobs.db` into `database/app.db`
- Updated routes so dashboard/add/edit/delete features run from `app.py`
- Updated route redirects from old index references to dashboard
- Removed old unused files:
  - `honey_app.py`
  - `database/jobs.db`
  - `merge_jobs_into_app.py`
  - `templates/index.html`

---

# Verified Working Features

- Create account
- Save user to database
- User login system
- Dashboard display
- Add application
- Edit application
- Delete application
- Status tracking
- Validation checks
- Weekly summary display

---

# Known Issues

- Password reset functionality has not been implemented yet
- Mobile responsiveness could be improved further
- Advanced filtering and sorting features are still limited
- Additional security improvements can be added for production deployment

---

# Future Enhancements

- Resume upload support
- Email notifications for application follow-ups
- Advanced search and filtering options
- Better analytics and reporting dashboard
- Calendar integration for interview scheduling
- Deployment to a cloud hosting platform

---

# Code Quality Notes

- The project follows Flask application structure
- SQLite is used for persistent data storage
- Validation is included for important form fields
- GitHub was used for version control and sprint collaboration
- Sensitive information such as passwords and API keys are not stored in the repository

---

# .gitignore Recommendation

Create a `.gitignore` file with the following:

```text
venv/
__pycache__/
*.pyc
database/app.db
.env
```

---

# Final Notes

This project helped the team improve skills in:
- Full-stack web development
- Flask routing and backend logic
- SQLite database management
- GitHub collaboration and version control
- Team communication and sprint planning

The Job Application Tracker demonstrates practical software development skills and collaborative teamwork through a complete capstone project.
