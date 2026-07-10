# Employee Project and Task Management System

A web-based full-stack task tracking dashboard designed for managers to assign tasks, check real-time completion status values, and manage project workflows through a centralized digital workspace.

## Features

- **Secure Manager Authentication**: Access validation connected straight to a secure database matching dedicated credentials.
- **Minimalist Capsule Design**: A clean dark bluish-grey scale design layout with rounded capsule styling inputs for modern aesthetics.
- **Dynamic Employee Context Resolution**: Toggling a task title instantly resolves down to its associated project workers without updating other employee progress bars.
- **Task Progression Tracker**: View historical logs, pull automated unique IDs from the database, and synchronize status changes instantly using modern Fetch API cycles.
- **Task Entry Registry**: Register new task lines into the MySQL infrastructure with automated auto-increment logic.

## Technology Stack

- **Frontend**: HTML5, CSS3 (Poppins Typography), Vanilla JavaScript (ES6+ Fetch APIs)
- **Backend**: Python 3.x, Flask Framework
- **Database**: MySQL Server

## File Structure

```text
Task-Management/           # Instructions telling Git to ignore venv/
│
├── static/                
│   ├── style.css          # Minimalist dark bluish-grey stylesheet
│   └── script.js          # Client-side dynamic API handlers
│
└── templates/             
│   ├── login.html         # Sign In view page layout
│   ├── dashboard.html     # Interactive primary manager dashboard
│   └── add_task.html      # Task insertion registry panel
├── app.py                 # Core Flask backend routes & APIs  
├── .gitignore
├── requirements.txt     # Python environment dependencies
