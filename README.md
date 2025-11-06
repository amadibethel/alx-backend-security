# IP Tracking & Anomaly Detection System

A **Django-based Security Application** that tracks and flags suspicious IP activities using **Celery** for background anomaly detection and provides **public Swagger API documentation**.

---

## Features

- Tracks IP addresses and logs requests.
- Detects anomalies (IPs exceeding 100+ requests/hour or hitting sensitive paths like `/admin`, `/login`).
- Sends email alerts for flagged IPs using Celery background tasks.
- Public Swagger documentation available at `/swagger/`.
- Celery + RabbitMQ integration for background task management.

---

## Tech Stack

| Component | Technology |
|------------|-------------|
| Framework | Django 4.2 |
| API Layer | Django REST Framework |
| Async Tasks | Celery 5 + RabbitMQ |
| Docs | drf-spectacular (Swagger/OpenAPI) |
| Email | Django SMTP backend |
| Server | Render / PythonAnywhere |
| Worker | Celery background worker |
| Language | Python 3.10+ |

---

## Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/amadibethel/alx-backend-security.git
cd alx-backend-security/ip_tracking


