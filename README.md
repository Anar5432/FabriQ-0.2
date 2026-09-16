# FabriQ 0.2 (Unified Textile ERP & Planning Platform)

This repository contains both the **Spring Boot** and **Python** implementations of the FabriQ Textile Production ERP and Planning Engine. Each implementation is contained in its own dedicated, independent folder.

---

## 📁 Repository Structure

```
FabriQ-0.2/
├── backend-spring/              # Java 21 & Spring Boot 3.3.1 Implementation
│   ├── src/main/java/           # REST APIs, JPA Entities, Planning Engine, Legacy MSSQL Sync
│   ├── src/main/resources/      # application.yml & Modular Web Frontend (css/, js/, index.html)
│   ├── src/test/java/           # Automated Unit & Mockito Test Suites
│   ├── pom.xml                  # Maven Dependencies & Plugins
│   ├── mvnw / mvnw.cmd          # Maven Wrapper
│   └── README.md                # Spring Boot specific documentation
│
└── backend-python/              # Python (FastAPI & Django) Implementation
    ├── dashboard/               # Planning engine, ERP connector, queries, queue engine
    ├── socks_dashboard/         # Django configuration & settings
    ├── static/                  # Python dashboard web assets (app.js, styles.css)
    ├── docs/                    # Architecture and logic maps
    ├── Database_Diagrams/       # DBML domain diagrams (sm_goods, sm_sob_trans, etc.)
    ├── investigation_scripts/   # Factory database exploration and verification scripts
    ├── main.py                  # FastAPI entry point & material reservation engine
    ├── manage.py                # Django administrative CLI
    ├── models.py & schemas.py   # SQLAlchemy domain models & Pydantic schemas
    ├── requirements.txt         # Python package dependencies
    ├── Dockerfile               # Container deployment specification
    └── README.md                # Python backend overview
```

---

## 🚀 Quick Navigation

### 1. Spring Boot Version (`/backend-spring`)
* **Tech Stack:** Java 21, Spring Boot 3.3.1, Spring Data JPA, Microsoft JDBC Driver, JUnit 5.
* **Frontend:** Modern Vanilla ES6 modules (`config.js`, `state.js`, `api.js`, `dashboard.js`, `planning.js`) and component CSS.
* **Features:** Dual MSSQL connection (`BTFERPDB` + `BTFERPDB_CORABA`), in-memory simulation engine, capacity constraint planning, BOM stock verification, and sub-order lifecycle tracking across Workwear, Underwear, and Socks.
* **To Run:**
  ```bash
  cd backend-spring
  ./mvnw spring-boot:run
  ```

### 2. Python Version (`/backend-python`)
* **Tech Stack:** Python 3.10+, FastAPI, Django, SQLAlchemy, PyMSSQL, Uvicorn.
* **Frontend:** Lightweight responsive dashboard (`static/`).
* **Features:** Raw legacy database queries, ERP queue sequencing, material reservations, and throughput analytics.
* **To Run:**
  ```bash
  cd backend-python
  pip install -r requirements.txt
  uvicorn main:app --reload --port 8000
  ```

---

## 📄 License
Internal proprietary software for factory operations.
