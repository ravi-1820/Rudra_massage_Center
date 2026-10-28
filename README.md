# Rudra Massage & Wellness

## Project Description

Rudra Massage & Wellness is a modern, full-stack massage therapy, spa, and wellness management platform built with Python (Django). It allows users to explore wellness equipment, browse therapy categories, view verified product specifications and intended uses, schedule consultation appointments, and calculate BMI.

The platform includes two dedicated applications: a front-facing `user` portal for clients to discover services, make appointments, submit inquiries, and request support, and a robust `admin` management dashboard for administrators to review appointments, manage catalog categories, oversee customer inquiries, and synchronize records with Google Sheets.

## Features

- **Service Catalog & Therapy Packages** -- Complete listing of wellness therapies and equipment categorized by health need, body part, and equipment type with detailed benefits, usage instructions, and safety precautions.
- **Client Booking & Appointments** -- Intuitive appointment scheduling workflow allowing clients to select preferred services, dates, and times with automated status tracking.
- **Customer Inquiry & Support System** -- Dedicated forms for general enquiries, clinic trial requests, and support tickets with admin response tracking.
- **Dedicated Custom Admin Dashboard** -- Clean, modern management dashboard with role-based access control, appointment approvals, category/service management, and quick metrics.
- **Google Sheets API Synchronization** -- Two-way integration allowing automated synchronization of enquiries and appointments directly to Google Sheets via Service Account credentials.
- **Bilingual & Localization Ready** -- Built-in English and Gujarati language support with persistent language switching and taxonomy translation catalogue.
- **Automated Data Seeder** -- Database seeder script to initialize default admin credentials, site settings, and verified core products.

## Windows

```cmd
# 1. Clone the repository
git clone https://github.com/ravi-1820/Rudra_massage_Center.git
cd Rudra_massage_Center/Rudra_Message_center

# 2. Setup
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Seed sample data (admin user, services, taxonomies)
python scripts/seed_data.py

# Start Django backend server
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## macOS / Linux

```bash
# 1. Clone the repository
git clone https://github.com/ravi-1820/Rudra_massage_Center.git
cd Rudra_massage_Center/Rudra_Message_center

# 2. Setup
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python3 manage.py migrate

# Seed sample data (admin user, services, taxonomies)
python3 scripts/seed_data.py

# Start Django backend server
python3 manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Credentials

- **Username:** admin
- **Email:** admin@gmail.com
- **Password:** admin
- **Admin Portal:** http://127.0.0.1:8000/admin/login/
- **Django Admin:** http://127.0.0.1:8000/django-admin/

## Screenshots

### 1. Home Page
![Home Page](Rudra_Message_center/Docs/Images/Home.jpeg)

### 2. Services & Products
![Services & Products](Rudra_Message_center/Docs/Images/Service_product.jpeg)

### 3. Login Page
![Login](Rudra_Message_center/Docs/Images/Login.jpeg)

### 4. Admin Dashboard
![Admin Dashboard](Rudra_Message_center/Docs/Images/Admin.jpeg)
