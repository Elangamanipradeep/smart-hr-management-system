# Smart HR Management System

## 📖 About the Project

Smart HR Management System is a modern Employee Management System built using Python and Django. It helps Human Resource (HR) teams efficiently manage employee information through a secure and user-friendly web application.

The system allows HR staff to perform complete employee management operations, including creating, viewing, updating, and deleting employee records. It also provides an interactive dashboard with employee statistics, department-wise analytics, and graphical reports to help HR monitor organizational data more effectively.

The project follows Django's best practices by implementing authentication, authorization, role-based permissions, profile photo management, and Git version control.

## ✨ Features

- Employee Management (Create, Read, Update & Delete)
- Employee Dashboard with Statistics
- Department-wise Analytics
- Interactive Charts using Chart.js
- Employee Profile Management
- Profile Photo Upload
- Automatic Old Profile Photo Cleanup
- Secure Login & Logout System
- Password Change Functionality
- User Authentication
- Role-Based Authorization
- Django Groups & Permissions
- Protected Routes using `login_required`
- Permission-Based Access Control
- Responsive User Interface
- Bootstrap 5 UI Design
- Git Version Control
- GitHub Repository Integration

## 🛠️ Technologies Used

### Backend
- Python 3
- Django

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Database
- SQLite

### Charts & Visualization
- Chart.js

### Version Control
- Git
- GitHub

## 📂 Project Structure

```text
Smart-HR-Management-System/
│
├── accounts/              # Authentication & User Management
├── config/                # Project Configuration
├── dashboard/             # Dashboard & Analytics
├── employees/             # Employee CRUD Module
├── static/                # CSS, JavaScript & Images
├── templates/             # HTML Templates
├── media/                 # Uploaded Employee Photos
├── manage.py              # Django Management Script
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Elangamanipradeep/smart-hr-management-system.git
```

### 2. Navigate to the project

```bash
cd smart-hr-management-system
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

### 5. Install project dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

## 🚀 Future Improvements

- REST API using Django REST Framework
- JWT Authentication
- React Frontend Integration
- AI-Powered HR Assistant
- Employee Attendance Management
- Leave Management System
- Payroll Management
- Email Notifications
- PostgreSQL Database Support
- Docker Deployment

## 👨‍💻 Author

**Elangamani Pradeep**

- GitHub: https://github.com/Elangamanipradeep
- Portfolio: https://elangamanipradeep.netlify.app/
