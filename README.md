## Health Monitoring & Telemedicine Platform

This is a Django 5 + Django REST Framework project for managing patients, consultations, analytics, and a web dashboard.

### 1. Requirements

- **Python**: 3.10+ (matching the version used by your `venv`)
- **Pip**: latest
- **Git** (optional, for cloning)

Python dependencies are listed in `requirements.txt`:
- `django==5.0.4`
- `djangorestframework==3.15.1`
- `djangorestframework-simplejwt==5.3.1`
- `django-cors-headers==4.3.1`

### 2. Setup & Installation

1. **Clone or copy the project**
   - Place the project in your desired folder (already under XAMPP `htdocs` in this setup).

2. **Create and activate a virtual environment (if you don’t want to use the existing `venv`)**

   ```bash
   # From the project root
   python -m venv venv

   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1

   # Windows (cmd)
   venv\Scripts\activate.bat
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

5. **(Optional) Create a superuser for the admin site**

   ```bash
   python manage.py createsuperuser
   ```

### 3. Running the Development Server

1. **Activate the virtual environment** (if not already active):

   ```bash
   .\venv\Scripts\Activate.ps1
   ```

2. **Start the Django server** from the project root (where `manage.py` lives):

   ```bash
   python manage.py runserver
   ```

3. **Access the app in your browser**
   - **Dashboard UI**: `http://127.0.0.1:8000/`
   - **Admin panel**: `http://127.0.0.1:8000/admin/`
   - **API root**: `http://127.0.0.1:8000/api/`

### 4. API & Authentication (brief)

- **JWT token endpoints**:
  - Obtain token: `POST /api/auth/token/`
  - Refresh token: `POST /api/auth/token/refresh/`
- Main API namespaces:
  - `GET /api/accounts/`
  - `GET /api/patients/`
  - `GET /api/consultations/`
  - `GET /api/analytics/`
  - `GET /api/dashboard/`

Use an HTTP client (e.g. Postman, Insomnia) and include the JWT access token in the `Authorization: Bearer <token>` header for protected endpoints.

