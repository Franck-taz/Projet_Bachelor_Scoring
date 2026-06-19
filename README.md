# Horizon Bank — Loan Risk Scoring Platform

A full-stack web application built as a Bachelor's thesis project, implementing an end-to-end loan risk assessment pipeline. Applicants submit loan requests through a client portal; a CatBoost machine learning model scores each application automatically; certified risk analysts review the AI prediction and issue the final lending decision.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [ML Model](#ml-model)
- [REST API](#rest-api)
- [Author](#author)

---

## Overview

The platform separates two distinct user roles:

| Role | Access | Responsibilities |
|---|---|---|
| **Client** | `/` | Register, submit loan applications, track status, read analyst messages |
| **Risk Analyst** | `/analyst/` | Review applications, consult AI risk score, approve or reject, add notes |

The AI scoring engine runs automatically after each submission, computing a **risk probability** (0–100 %) using a trained CatBoost classifier. Analysts can override the AI prediction at any time — in compliance with GDPR Article 22, no decision is ever made solely by the algorithm.

---

## Features

### Client Portal
- Account registration and login
- Multi-step loan application form with real-time field validation
- Pre-submission review page with application summary
- Personal dashboard listing all applications and their statuses
- Messaging inbox to read notes left by the assigned analyst
- Document upload (pay slips, rent receipts, work contracts, etc.)

### Analyst Portal
- Dedicated login (staff accounts only)
- Dashboard with KPI cards (awaiting review, approved, high risk) and a bar chart
- Search and filter applications by prediction or decision status
- Detailed application view: full client profile, financial data, uploaded documents
- Inline AI risk score with colour-coded progress bar (Low / Medium / High)
- Final decision dropdown (Approve / Reject) with AJAX save
- Analyst notes system linked to each application

### General
- Fully responsive UI — tested at 320 px, 360 px, 480 px, 768 px, 1024 px+
- OpenAPI schema auto-generated with drf-spectacular (Swagger UI at `/api/docs/`)
- Legal notice and privacy policy page (GDPR-compliant)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Web framework | Django 6.0.1 |
| ML model | CatBoost 1.2+ |
| Data processing | pandas, scikit-learn, NumPy |
| REST API | Django REST Framework + drf-spectacular |
| Frontend | Vanilla HTML/CSS/JS (no framework) |
| Database | PostgreSQL 18 (psycopg2-binary) |
| Package manager | [uv](https://github.com/astral-sh/uv) |

---

## Project Structure

```
Projet_Bachelor_Scoring/
│
├── loan_manager/                 # Main Django application
│   ├── models.py                 # LoanApplication, AnalystNote, Document, profiles
│   ├── views.py                  # Client-facing views
│   ├── analyst_views.py          # Analyst portal views
│   ├── api_views.py              # REST prediction endpoint
│   ├── forms.py                  # Loan application form + validation
│   ├── serializers.py            # DRF serializers
│   ├── urls.py                   # Client URL routes
│   ├── analyst_urls.py           # Analyst URL routes
│   ├── ml/
│   │   └── predictor.py          # Feature engineering + CatBoost inference
│   ├── static/css/               # Stylesheets
│   └── templates/loan_manager/   # HTML templates
│       ├── base.html
│       ├── login.html / register.html
│       ├── dashboard.html
│       ├── apply.html / review.html / success.html
│       ├── messages.html
│       ├── about.html / legal.html
│       └── analyst/
│           ├── login.html
│           ├── dashboard.html
│           └── detail.html
│
├── Models/
│   ├── best_model.cbm            # Trained CatBoost model
│   ├── column_transformer.pkl    # Fitted sklearn ColumnTransformer
│   └── metadata.json             # Training metadata and feature list
│
├── Notebooks/
│   └── Scoring.ipynb             # Model training and evaluation notebook
│
├── Data/
│   ├── TrainingData.csv
│   ├── TestData.csv
│   └── Sample Prediction Dataset.csv
│
├── projet_bachelor_scoring/      # Django project settings
│   ├── settings.py
│   └── urls.py
│
├── manage.py
├── pyproject.toml
├── requirements.txt              # Pinned dependencies for pip (Render)
├── render.yaml                   # Render deployment blueprint
├── build.sh                      # Render build script
├── db_dump.json                  # Django fixture (JSON)
├── db_dump.sql                   # PostgreSQL dump (SQL)
└── .env                          # Environment variables (not committed)
```

---

## Getting Started

### Prerequisites

- Python 3.12
- [uv](https://github.com/astral-sh/uv) (recommended) **or** pip

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Projet_Bachelor_Scoring

# Create virtual environment and install dependencies with uv
uv sync

# Or with pip
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e .
```

### Environment Variables

Create a `.env` file at the project root:

```env
DB_NAME=loan_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

In production (Render), the following variables are set automatically:

```env
DATABASE_URL=postgresql://...    # provided by Render PostgreSQL
SECRET_KEY=...                   # auto-generated
DEBUG=False
ALLOWED_HOSTS=.onrender.com
```

### Database Setup

```bash
python manage.py migrate
python manage.py loaddata db_dump.json
```

### Create an Analyst Account

Analyst accounts require `is_staff=True`. Create one via the Django shell:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from loan_manager.models import AnalystProfile

user = User.objects.create_user(
    username='analyst@horizonbank.com',
    email='analyst@horizonbank.com',
    password='yourpassword',
    first_name='Jane',
    last_name='Doe',
    is_staff=True
)
AnalystProfile.objects.create(user=user, employee_id='EMP-001')
```

### Run the Development Server

```bash
python manage.py runserver
```

The application is available at `http://127.0.0.1:8000`.

---

## Usage

### Test Accounts

#### Analyst (back-office)

| Email | Password | Access |
|---|---|---|
| `marie-analyst@horizonbank.com` | `Analyst2026!` | Analyst dashboard + Django admin (`/admin/`) |

#### Clients

| Name | Email | Password |
|---|---|---|
| John Doe | `johndoe@gmail.com` | `John2026!` |
| Alice Martin | `alice.martin@gmail.com` | `Alice2026!` |
| Bob Smith | `bob.smith@gmail.com` | `BobSmith26!` |
| Clara Dupont | `clara.dupont@gmail.com` | `Clara2026!` |
| David Kumar | `david.kumar@gmail.com` | `DavidK26!` |
| Emma Wilson | `emma.wilson@gmail.com` | `EmmaW2026!` |
| Farid Benali | `farid.benali@gmail.com` | `Farid2026!` |
| Grace Chen | `grace.chen@gmail.com` | `GraceC2026!` |
| Hugo Rossi | `hugo.rossi@gmail.com` | `HugoR2026!` |
| Ines Nakamura | `ines.nakamura@gmail.com` | `InesN2026!` |

#### Django Admin

Access the Django admin back-office at `/admin/` using the analyst credentials above.

### Client Portal

| URL | Description |
|---|---|
| `/` | Login |
| `/register/` | Create a client account |
| `/dashboard/` | Application history and statuses |
| `/apply/` | New loan application form |
| `/apply/review/` | Pre-submission summary |
| `/success/` | Confirmation page |
| `/messages/` | Analyst notes inbox |
| `/profile/` | View/edit profile, delete account |

### Analyst Portal

| URL | Description |
|---|---|
| `/analyst/login/` | Analyst login |
| `/analyst/dashboard/` | All applications + KPIs + chart |
| `/analyst/application/<id>/` | Full detail view for one application |
| `/admin/` | Django admin back-office |

---

## ML Model

### Architecture

The scoring engine is a **CatBoostClassifier** trained to predict credit default risk (`Risk_Flag`). It was trained on a labeled dataset of historical loan applications.

**Training configuration** (see `Models/metadata.json`):

| Parameter | Value |
|---|---|
| Iterations | 500 |
| Learning rate | 0.1 |
| Tree depth | 8 |
| L2 regularisation | 3 |
| Class weights | `[1, 6]` (handles class imbalance) |
| Eval metric | AUC |
| Optimal threshold | ~0.50 |

### Feature Engineering (`loan_manager/ml/predictor.py`)

Raw applicant data is transformed before inference:

| Engineered feature | Description |
|---|---|
| `income_per_age` | Annual income divided by age |
| `married_owns_house` | Binary: married AND owns home |
| `owns_car_high_income` | Binary: owns car AND income above median |
| `age_bin` | Age bucketed into 5 ranges (21-30, …, 61-80) |
| `experience_bin` | Experience bucketed into 5 ranges |
| `income_bin` | Income bucketed in 2 M increments |
| `cur_job_years_bin` | Current job tenure bucketed into 4 ranges |

A `ColumnTransformer` (serialised as `column_transformer.pkl`) applies standard scaling to numeric features and one-hot encoding to categoricals before the model receives the data.

### Risk Output

`predict_risk()` returns a **float between 0 and 1** representing the probability of default. The application maps this to a label:

| Score | Risk level | AI Prediction |
|---|---|---|
| < 30 % | Low | Approved |
| 30 % – 80 % | Medium | Pending |
| > 80 % | High | Rejected |

The final lending decision always belongs to a human analyst who may override the AI prediction.

---

## REST API

### `POST /api/predict/`

Run the risk model on an applicant's data.

**Request body:**

```json
{
  "age": 35,
  "income": 60000,
  "experience": 8,
  "cur_job_years": 3,
  "current_house_yrs": 5,
  "loan_amount": 20000,
  "marital_status": "married",
  "house_ownership": "rented",
  "car_ownership": "yes",
  "region": "North India",
  "job_category": "Technology & IT"
}
```

**Response:**

```json
{
  "risk_score": 0.234,
  "risk_flag": 0,
  "prediction": "Approved"
}
```

Full interactive documentation is available at `/api/docs/` (Swagger UI).

---

## Deployment

The application is deployed on **Render** (PaaS).

| Component | Service |
|---|---|
| Web server | Gunicorn (WSGI) |
| Static files | WhiteNoise (compressed + cache-busted) |
| Database | Render PostgreSQL (free tier) |
| Blueprint | `render.yaml` (infrastructure as code) |

To deploy from scratch:

1. Push the repository to GitHub
2. On Render → **New** → **Blueprint** → select the repo
3. `render.yaml` automatically provisions the web service + PostgreSQL database
4. Create an analyst account via Render Shell: `python manage.py shell`

---

## Author

**Franck Tazesimo**  
Bachelor's thesis — 2026
