# Domestic Abuse Support and Legal Aid System

> A secure, role-based case management platform built with Django to support survivors of domestic abuse through structured professional coordination and confidential communication.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [User Roles](#user-roles)
- [Technical Architecture](#technical-architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Demonstration Workflow](#demonstration-workflow)
- [Security & Privacy](#security--privacy)
- [Contributing](#contributing)

---

## Overview

The **Domestic Abuse Support and Legal Aid System** is a web application designed to provide a structured, confidential environment for survivors of domestic abuse. It facilitates coordinated case management between survivors, counsellors, legal advisors, and administrators — enforcing strict role-based access control at every level.

The platform prioritises survivor privacy and dignity through case-bound communication channels, ensuring that sensitive interactions remain accessible only to directly involved parties.

---

## Key Features

| Feature | Description |
|---|---|
| Survivor Self-Registration | Survivors can independently register and manage their accounts |
| Role-Based Access Control | Strict permission enforcement across all user types |
| Help Request Management | Survivors submit and track requests through a dedicated interface |
| Administrative Case Assignment | Administrators coordinate and distribute cases to professionals |
| Secure Case Messaging | Encrypted, case-scoped communication between survivors and assigned professionals |
| Role-Based Dashboard Routing | Each user is directed to a tailored dashboard upon login |
| Privacy-First Design | Administrators have no access to private survivor–professional communications |

---

## User Roles

### Survivor
- Register and authenticate with the system
- Submit and track help requests
- Communicate securely with assigned counsellors and legal advisors

### Administrator
- View and manage all submitted help requests
- Assign counsellors and legal advisors to cases
- Oversee system flow and case distribution
- **No access** to private survivor–professional communications

### Counsellor
- View cases they have been assigned to
- Communicate securely with assigned survivors

### Legal Advisor
- View cases they have been assigned to
- Communicate securely with assigned survivors

---

## Technical Architecture

The system follows a modular Django architecture with clear separation of concerns across dedicated applications.

| Application | Responsibility |
|---|---|
| `accounts` | Custom user model and authentication logic |
| `support` | Help request creation and case assignment workflows |
| `communication` | Secure, case-scoped messaging system |
| `core` | Dashboard routing and role-based redirection |
| `resources` | Informational content management |

**Core implementation highlights:**

- `CustomUser` model with a `role` field driving access control
- Class-based views (CBVs) for clean, reusable logic
- `ModelForms` for structured and validated input handling
- `LoginRequiredMixin` enforcing authentication on all protected routes
- Role validation at the view level for fine-grained permission checks
- Secure POST-based logout to prevent CSRF vulnerabilities
- SQLite for development; PostgreSQL-ready configuration for production

---

## Project Structure

```
DomesticAbuseSupport/
├── manage.py
├── requirements.txt
├── dv_support/             # Project settings and URL configuration
├── accounts/               # User model and authentication
├── support/                # Help requests and case assignment
├── communication/          # Secure case-based messaging
├── core/                   # Dashboard routing and role redirection
├── resources/              # Informational content
├── templates/              # HTML templates
└── static/                 # Static assets (CSS, JS, images)
```

> The following are excluded from version control: `venv/`, `db.sqlite3`, `__pycache__/`, `.env`

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/n4ku7/DomesticAbuseSupport.git
cd DomesticAbuseSupport
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Create an Administrator Account

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password for the admin account.

### 6. Start the Development Server

```bash
python manage.py runserver
```

The application will be available at: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## Demonstration Workflow

The following sequence demonstrates the full system workflow, role separation, and access control mechanisms:

1. **Register** a new survivor account via the registration page
2. **Submit a help request** from the survivor dashboard
3. **Log in as administrator** and assign a counsellor and legal advisor to the case
4. **Log in as counsellor** and access the assigned case from the counsellor dashboard
5. **Send a message** to the survivor via the secure messaging system
6. **Log in as survivor** and respond to the counsellor's message

This flow validates the complete lifecycle of a case, from initial submission through professional assignment and confidential communication.

---

## Security & Privacy

- All routes require authentication via `LoginRequiredMixin`
- Role-based validation is enforced at the view level; no role can access resources outside its scope
- Case-bound messaging ensures communications are never exposed across unrelated cases
- Administrator accounts are explicitly restricted from accessing private survivor–professional conversations
- Logout is handled via a secure POST request to mitigate CSRF risks
- Sensitive configuration (secret keys, database credentials) is managed through environment variables (`.env`) and excluded from version control

---

## Contributing

Contributions, suggestions, and issue reports are welcome. Please open an issue or submit a pull request via the [GitHub repository](https://github.com/n4ku7/DomesticAbuseSupport).

When contributing, ensure that any changes:
- Maintain or strengthen existing access control and privacy mechanisms
- Follow the established modular Django application structure
- Include appropriate documentation for new features or changes

---

*This project was developed to simulate a structured support environment for survivors of domestic abuse. It is intended for educational and demonstration purposes.*