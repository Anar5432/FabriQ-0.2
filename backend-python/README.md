# FabriQ Python Backend

This directory contains the Python version of the FabriQ ERP and Planning Engine built with **FastAPI** and **Django**.

## Architecture & Modules
- **FastAPI Core (`main.py`)**: REST endpoints for orders, material reservations, and live sector metrics.
- **Data Layer (`models.py`, `schemas.py`, `database.py`)**: SQLAlchemy ORM models, Pydantic validation schemas, and database session handling.
- **Dashboard App (`dashboard/`)**: Planning engine, queue sequencing (`queue_engine.py`), throughput engine (`throughput_engine.py`), material stock validation (`material_checker.py`), and legacy SQL query builders (`queries.py`).
- **Socks Factory App (`socks_dashboard/`)**: Django settings and routing.
- **Static Frontend (`static/`)**: Python dashboard HTML, CSS, and JS.
- **Investigation Scripts (`investigation_scripts/`)**: Detailed diagnostic and exploration scripts querying `BTFERPDB` and `BTFERPDB_CORABA`.

## Setup & Execution
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
