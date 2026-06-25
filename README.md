# TicketFlow-Ticket Management System

A Django-based ticket management system with role-based access for admins and regular users.

## Features

### Admin
- View and manage all users and their profiles
- Create, update, delete tickets for any user
- Filter tickets by user, status, and priority
- Kanban-style dashboard showing all users' tickets with live stats

### User
- Register and manage personal profile
- Create and manage own tickets with due dates
- View tickets in a Kanban-style dashboard
- Update ticket status and priority
- See overdue ticket highlighting

## Tech Stack
- **Backend:** Django 5.2.3
- **Database:** SQLite3
- **Frontend:** Bootstrap 5.3, custom CSS
- **Auth:** Django built-in authentication


## Project Structure
```text
├── core/                     # Django settings, root URLs, WSGI
├── tickets/                  # Ticket management app
│   ├── templates/            # Ticket-related HTML templates
│   └── static/
│       └── tickets/          # Ticket-specific CSS
├── account/                  # User authentication and profile app
│   ├── templates/            # Authentication/profile HTML templates
│   └── static/
│       └── account/          # Account-specific CSS and JS
└── templates/                # Shared base template (base.html)
```

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Rameen07304/jira-ticket-system.git

```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Open .env and fill in your values
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |

## Usage

- **Admin login** → sees User List, Homepage, and Tickets dropdown (Own + User Tickets)
- **Regular user login** → sees Tickets and Homepage only
- **Profile** → accessible from navbar dropdown for all users
