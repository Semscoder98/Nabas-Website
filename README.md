# NABAS Web Portal - Full Django & Frontend System

Official Web Portal and Administrative Management System for the **National Association of Badagry Students (NABAS)**.

---

## 🚀 Quick Start Guide

### 1. Activate the Virtual Environment
On Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```
Or on Command Prompt:
```cmd
.\.venv\Scripts\activate.bat
```

### 2. Run Database Migrations (already initialized)
```bash
python manage.py migrate
```

### 3. Run the Development Server
```bash
python manage.py runserver
```

Open your browser at:
- **Public Portal**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Administrative Dashboard**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔐 Administrative Credentials
- **Username**: `admin`
- **Password**: `admin123`
*(Remember to change the password in production)*

---

## 📁 Project Architecture

```
nabweb/
├── .venv/                      # Python Virtual Environment
├── db.sqlite3                  # SQLite Database (seeded with realistic Badagry data)
├── manage.py                   # Django CLI Tool
├── requirements.txt            # Python Dependencies
├── seed_db.py                  # Database Seeding Utility
│
├── nabas_project/              # Core Project Settings
│   ├── settings.py             # App configurations, templates, media, static settings
│   ├── urls.py                 # Master URL Routing
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── core/                   # Home, About, Leadership, Contact, Gallery, Donations
│   ├── members/                # Student Registration, Digital ID Cards, Campus Chapters
│   ├── news/                   # Articles, Categories, Announcements, Comments
│   └── programs/               # Flagship Events, Scholarships, Resource Library
│
├── templates/
│   ├── base.html               # Universal Navbar, Footer, Mobile Drawer & Flash Alerts
│   ├── 404.html                # Custom 404 Page Not Found
│   ├── 500.html                # Custom 500 Server Error
│   ├── core/                   # index.html, about.html, leadership.html, contact.html, etc.
│   ├── members/                # campus.html, registration.html
│   ├── news/                   # news_list.html, news_detail.html
│   └── programs/               # program_list.html, scholarship_list.html, resource_list.html
│
├── static/                     # Static CSS, JS, and Brand Assets
└── media/                      # Uploaded Passports, News Cover Images, and PDF Documents
```

---

## 🌟 Key Features Integrated

1. **Template Inheritance (`base.html`)**:
   - Centralized navigation bar with active route highlighting.
   - Dynamic mobile menu and scroll animations.
   - Unified footer with contact details, Badagry Secretariat address, and social links.
   - Global Django flash message banner for form feedback.

2. **Student Membership & Digital ID Card Generator**:
   - 4-step interactive registration wizard.
   - Standard CR80 two-sided digital student ID with barcode.
   - Automated registration into Django's backend database (`Member` model).
   - Instant isolated card printing (`window.print()`).

3. **Django Admin Management Panel**:
   - Full CRUD control for Executive Council profiles, Campus Chapters, News Articles, Scholarships, Downloads, and Donations.
   - Search, filter, and export capabilities.

4. **Dynamic News & Blog Bureau**:
   - Search articles by keyword or category.
   - Reading view with comment threads, view counters, and related articles.

5. **Contact & Donation Tracking**:
   - Messages sent from the contact form save directly to `ContactMessage` in the admin panel.
   - Donations recorded with reference tracking and status flags.
