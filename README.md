# 🎓 Streamlit PostgreSQL Opportunity Dashboard

**University of Central Punjab — Tools & Techniques for Data Science**
**Assignment #4 | Department of Applied Computing & Technologies**

---

## 📋 Project Overview

A full-stack **Internship & Job Tracking Dashboard** built with:

| Layer        | Technology                     |
|--------------|-------------------------------|
| Frontend     | Streamlit (Python)            |
| Database     | PostgreSQL 16                 |
| DB Admin     | pgAdmin 4                     |
| ORM          | SQLAlchemy 2.0 + psycopg2     |
| Charts       | Plotly Express                |
| Containers   | Docker Compose                |
| Auth         | Streamlit session_state       |

---

## 🏗️ Architecture

```
User Browser
     │
     ▼
Streamlit App (port 8501)
     │
     ▼
PostgreSQL (port 5432)  ◄───►  pgAdmin (port 5050)
     │
     ▼
Docker Named Volume (postgres_data)

GitHub ──► Source code, commits, documentation
```

---

## 📁 Folder Structure

```
streamlit-postgres-assignment/
├── app/
│   ├── main.py                     # Entrypoint + navigation
│   ├── db.py                       # SQLAlchemy engine + connection
│   ├── queries.py                  # All CRUD + analytics queries
│   ├── auth.py                     # Login / session state / roles
│   ├── utils.py                    # Shared helpers, validation
│   └── pages/
│       ├── 0_Home.py
│       ├── 1_Add_Opportunity.py
│       ├── 2_View_Search.py
│       ├── 3_Update_Opportunity.py
│       ├── 4_Delete_Opportunity.py
│       ├── 5_Analytics_Dashboard.py
│       ├── 6_CSV_Upload_Export.py
│       ├── 7_Duplicate_Detection.py
│       ├── 8_Deadline_Alerts.py
│       └── 9_Database_Health_Check.py
├── database/
│   ├── init.sql                    # Table schema + indexes
│   └── seed_data.sql               # 40+ sample records
├── screenshots/                    # Add screenshots here
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop (running)
- Git
- VS Code (recommended)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-org/streamlit-postgres-assignment.git
cd streamlit-postgres-assignment

# 2. Copy environment file
cp .env.example .env

# 3. Build and start all services
docker compose up -d --build

# 4. Check all containers are running
docker compose ps
```

Then open:
- **Streamlit App** → http://localhost:8501
- **pgAdmin**        → http://localhost:5050

---

## 🔑 Login Credentials

| Username | Password   | Role   |
|----------|-----------|--------|
| `admin`  | `admin123` | Admin  |
| `viewer` | `viewer123`| Viewer |
| `faculty`| `ucp2026`  | Admin  |

**Admin** → Full access (Add, Update, Delete, CSV Upload)
**Viewer** → Read-only (View, Analytics, Export, Health Check)

---

## 🐳 Docker Compose Services

| Service           | Image                   | Port       | Purpose                       |
|-------------------|------------------------|------------|-------------------------------|
| `postgres_db`     | `postgres:latest`       | 5432:5432  | PostgreSQL database           |
| `pgadmin`         | `dpage/pgadmin4:latest` | 5050:80    | pgAdmin web UI                |
| `streamlit_app`   | Built from Dockerfile   | 8501:8501  | Streamlit application         |

### Key Docker Compose Concepts

| Concept               | Explanation                                                   |
|-----------------------|---------------------------------------------------------------|
| `services`            | Defines each container in the stack                          |
| `image`               | Docker Hub image to pull                                     |
| `build`               | Builds from local Dockerfile instead of pulling              |
| `container_name`      | Friendly name for the container                              |
| `ports`               | Maps `host:container` ports                                  |
| `environment`         | Sets environment variables inside the container              |
| `volumes`             | Mounts host paths or named volumes                           |
| `depends_on`          | Start order dependency with `condition: service_healthy`     |
| `restart`             | `unless-stopped` restarts container on crash                 |
| Docker network        | All services share one default network automatically         |
| Service name routing  | Streamlit connects to `postgres_db` (service name as host)   |

---

## 🗄️ Database

**Database:** `student_opportunities_db`
**Table:** `opportunities`

| Column                | Type           | Notes                              |
|-----------------------|----------------|------------------------------------|
| opportunity_id        | SERIAL PK      | Auto-increment primary key         |
| company_name          | VARCHAR(100)   | NOT NULL                           |
| job_title             | VARCHAR(150)   | NOT NULL                           |
| category              | VARCHAR(50)    | NOT NULL                           |
| city / country        | VARCHAR(80)    |                                    |
| work_mode             | VARCHAR(30)    | CHECK: Remote/Onsite/Hybrid        |
| required_skills       | TEXT           | NOT NULL                           |
| salary_min/max        | NUMERIC(10,2)  |                                    |
| currency              | VARCHAR(10)    | Default: PKR                       |
| experience_level      | VARCHAR(50)    |                                    |
| application_deadline  | DATE           |                                    |
| status                | VARCHAR(30)    | CHECK: Open/Closed/Expired/Shortlisted |
| source_link           | TEXT           |                                    |
| created_at            | TIMESTAMP      | Default: CURRENT_TIMESTAMP         |

Seed data includes **42 records** from **6 companies**, **5 cities**, **4 categories**.

---

## 🖥️ pgAdmin Setup

1. Open http://localhost:5050
2. Login: `admin@example.com` / `admin123`
3. Right-click **Servers → Register → Server**
4. **General:** Name = `Opportunity DB`
5. **Connection:**
   - Host: `postgres_db` ← Docker service name
   - Port: `5432`
   - Database: `student_opportunities_db`
   - Username: `app_user`
   - Password: `app_password`
6. Save and browse the table under Schemas → public → Tables

---

## 🐳 Useful Docker Commands

```bash
docker compose up -d             # Start all services (detached)
docker compose up -d --build     # Rebuild Streamlit image and start
docker compose ps                # Check running containers + ports
docker compose logs postgres_db  # PostgreSQL logs
docker compose logs pgadmin      # pgAdmin logs
docker compose logs streamlit_app # Streamlit logs
docker compose down              # Stop containers (keep volumes)
docker compose down -v           # Stop and DELETE volumes (data lost!)
docker volume ls                 # List all Docker volumes
docker volume inspect streamlit-postgres-assignment_postgres_data
```

---

## 🔧 GitHub Workflow

```bash
# Initial setup
git init
git add .
git commit -m "initial project structure"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main

# Daily workflow
git status
git add app/pages/1_Add_Opportunity.py
git commit -m "add opportunity form with validation"
git push
```

Every group member must make **at least 5 meaningful commits** distributed across the project timeline.

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5432 in use | Stop local PostgreSQL: `net stop postgresql` (Windows) |
| Port 5050 in use | Change to `5051:80` in docker-compose.yml |
| Port 8501 in use | Change to `8502:8501` in docker-compose.yml |
| pgAdmin can't connect | Use `postgres_db` as host (not `localhost`) |
| Streamlit DB error | Check DB_HOST is `postgres_db` in environment |
| Data gone after restart | Never use `docker compose down -v` in production |
| Table does not exist | Check init.sql is mounted correctly; re-run `docker compose down -v && docker compose up -d` |
| Git push rejected | `git pull --rebase origin main` then push again |

---

## 👥 Team Contribution

| Name | GitHub Username | Tasks |
|------|----------------|-------|
| Member 1 | @username1 | DB schema, seed data, queries.py |
| Member 2 | @username2 | Streamlit pages, analytics dashboard |
| Member 3 | @username3 | Docker setup, README, report |

---

## 📚 References

- [Streamlit Docs](https://docs.streamlit.io/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [pgAdmin Container Docs](https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html)
- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/en/20/)
- [Plotly Python Docs](https://plotly.com/python/)
