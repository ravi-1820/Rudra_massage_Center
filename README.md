# Rudra Massage Center

## Project Description

Rudra Massage Center is a comprehensive spa and wellness management web platform built with Django. It provides an intuitive, reliable system for clients to explore massage treatments, therapeutic sessions, and wellness packages, and easily schedule appointments online with real-time availability.

The platform includes two dedicated applications: a front-facing `user` application for clients to discover services, make appointments, and view booking history, and a robust `admin` management portal for therapists and administrators to handle appointments, manage service offerings, review client inquiries, and oversee day-to-day spa operations.

## Features

- **Service Catalog & Therapy Packages:** Complete listing of massage therapies, wellness sessions, durations, and pricing with detailed descriptions.
- **Client Booking & Appointments:** Intuitive appointment scheduling system allowing clients to select preferred dates, time slots, and therapists.
- **User Management & Profiles:** User registration, secure login, profile management, and appointment history tracking.
- **Dedicated Admin Portal:** Tailored management dashboard for staff and administrators to approve appointments, update schedules, and manage services.
- **Built-in Django Admin Interface:** Complete control over backend models, user roles, authentication, and database records.
- **Responsive & Modern Design:** Fully responsive layout optimized for desktop, tablet, and mobile browsers.

## Windows

```cmd
# 1. Clone the repository
git clone <repository-url>
cd Rudra_massage_center

# 2. Create virtual environment
python -m venv env

# 3. Activate virtual environment
env\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser (Optional / Pre-configured)
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## macOS / Linux

```bash
# 1. Clone the repository
git clone <repository-url>
cd Rudra_massage_center

# 2. Create virtual environment
python3 -m venv env

# 3. Activate virtual environment
source env/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser (Optional / Pre-configured)
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Credentials

- **Username:** admin
- **Email:** admin@gmail.com
- **Password:** admin
