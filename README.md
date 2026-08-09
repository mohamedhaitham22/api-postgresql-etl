# 🛒 FakeStore API to PostgreSQL ETL Pipeline

An end-to-end Python-based ETL (Extract, Transform, Load) data pipeline that extracts product data from the [DummyJSON API](https://dummyjson.com), persists raw JSON data locally for auditing, normalizes nested payload data into relational schemas, and loads it into a **PostgreSQL** database with **upsert support**.

---

## 📋 Table of Contents
- [Features](#-features)
- [Architecture & Data Flow](#-architecture--data-flow)
- [Technologies Used](#-technologies-used)
- [Database Schema](#-database-schema)
- [Project Structure](#-project-structure)
- [Getting Started & Setup](#-getting-started--setup)
  - [Option 1: Docker & Airflow Setup (Recommended)](#option-1-docker--airflow-setup-recommended)
  - [Option 2: Local Python Setup](#option-2-local-python-setup)
- [Analytics & Verification](#-analytics--verification)

---

## ✨ Features

- **Extract**: Retrieves batch product data from external REST APIs using a resilient HTTP client (`requests.Session` with timeout and error handling).
- **Raw Persistence**: Saves raw timestamped JSON snapshots under `data/raw/` for auditing and data lineage.
- **Transform**: Normalizes complex nested JSON payloads (dimensions, tags, reviews, metadata, images) into clean relational structures.
- **Load (PostgreSQL)**: Transactionally upserts (`ON CONFLICT DO UPDATE / DO NOTHING`) data into PostgreSQL database tables.
- **Orchestration**: Scheduled automated execution via **Apache Airflow** DAG (`product_etl_pipeline`).
- **Containerized Stack**: Complete **Docker Compose** environment bundling PostgreSQL 17, pgAdmin 4, and Apache Airflow.
- **Robust Configuration**: Strongly typed settings management powered by `pydantic-settings` reading from `.env`.
- **Centralized Logging**: Formatted dual logging to file (`logs/etl.log`) and console output (`stdout`) for observability.

---

## 🏗️ Architecture & Data Flow

```
+-------------------+        +--------------------+        +---------------------+
| DummyJSON API     | -----> |  Extract Layer     | -----> |  Local Storage      |
| (/products)       |        |  (APIClient)       |        |  (data/raw/*.json)  |
+-------------------+        +--------------------+        +---------------------+
                                       |
                                       v
                             +--------------------+
                             |  Transform Layer   |
                             |  (Normalization)   |
                             +--------------------+
                                       |
                                       v
                             +--------------------+
                             |    Load Layer      |
                             |  (PostgreSQL Raw)  |
                             +--------------------+
```

### Pipeline Steps:
1. **APIClient** makes an HTTP GET request to retrieve product data.
2. **LocalStorage** persists the raw JSON payload to `data/raw/products/YYYYMMDD_HHMMSS.json`.
3. **Transformer** parses and separates raw payloads into 6 relational entities: `products`, `product_dimensions`, `product_tags`, `product_reviews`, `product_metadata`, and `product_images`.
4. **Loader** opens a PostgreSQL transaction via **SQLAlchemy engine** and executes database upserts.

---

## 🛠️ Technologies Used

- **Language**: Python 3.12+
- **Orchestration**: Apache Airflow 2.10+
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 17
- **Database Administration**: pgAdmin 4
- **Database Connector**: SQLAlchemy 2.0+, `psycopg2-binary`
- **HTTP Client**: `requests`
- **Configuration & Validation**: Pydantic v2, `pydantic-settings`
- **Data Processing**: `pandas`
- **Code Quality**: `ruff`, `black`, `mypy`, `pytest`

---

## 🗄️ Database Schema

The pipeline populates the **`raw`** schema in PostgreSQL:

| Table Name | Description | Key / Constraint |
| :--- | :--- | :--- |
| **`raw.products`** | Main product details (title, price, stock, brand, SKU, etc.) | `PRIMARY KEY (product_id)` |
| **`raw.product_dimensions`** | Product width, height, and depth | `PRIMARY KEY (product_id)`, FK to `products` |
| **`raw.product_tags`** | Associated tag labels | `PRIMARY KEY (product_id, tag)`, FK to `products` |
| **`raw.product_reviews`** | Customer ratings, comments, and reviewer info | `PRIMARY KEY (review_id)`, FK to `products` |
| **`raw.product_metadata`** | Barcodes, QR codes, and timestamp metadata | `PRIMARY KEY (product_id)`, FK to `products` |
| **`raw.product_images`** | Product image URLs | `PRIMARY KEY (image_id)`, FK to `products` |

---

## 📁 Project Structure

```
etl-fakestore/
├── airflow/                  # Airflow DAGs, plugins, and execution logs
│   └── dags/
│       └── product_etl_dag.py # Airflow ETL DAG definition
├── docker/                   # Docker build context
│   ├── Dockerfile
│   └── requirements.txt
├── sql/
│   ├── creation.sql          # DDL script for PostgreSQL schema, tables, and indexes
│   └── analytics_queries.sql # Analytical SQL queries for data reporting
├── src/
│   ├── clients/              # HTTP API client module
│   ├── config/               # Pydantic settings & environment configuration
│   ├── database/             # Database connection & SQLAlchemy engine
│   ├── extract/              # Data extraction module
│   ├── storage/              # Raw local JSON persistence module
│   ├── transform/            # Normalization & parsing logic
│   ├── load/                 # Database loading & upsert logic
│   ├── utils/                # Logging setup
│   └── main.py               # Main pipeline execution entrypoint
├── .env.example              # Template for environment variables
├── .gitignore                # Git ignore rules
├── docker-compose.yml        # Multi-container orchestration (Airflow + PostgreSQL + pgAdmin)
├── pyproject.toml            # Python dependencies and build config
└── README.md                 # Project documentation
```

---

## ⚙️ Getting Started & Setup

Choose one of the setup options below to run the pipeline:

### Option 1: Docker & Airflow Setup (Recommended)

Run the complete pipeline stack—including PostgreSQL 17, pgAdmin 4, and Apache Airflow—in containerized environment using Docker Compose.

#### Prerequisites
- **Docker Engine** & **Docker Compose** installed on your system.

#### 1. Environment Configuration
Copy `.env.example` to create `.env`:

```bash
cp .env.example .env
```
Ensure all required configuration variables are populated in `.env`.

#### 2. Launch Container Stack
Start all services in detached mode:

```bash
docker compose up -d
```

This starts the following services:
- **`airflow-postgres`**: PostgreSQL 17 container (Exposed on port `5433`).
- **`pgadmin`**: pgAdmin 4 web management tool (Exposed on port `5050`).
- **`airflow-init`**: One-time database migration and admin user creation task.
- **`airflow-webserver`**: Airflow Web Interface (Exposed on port `8080`).
- **`airflow-scheduler`**: Airflow Scheduler managing DAG execution.

#### 3. Database Schema Initialization
Execute `sql/creation.sql` against the running PostgreSQL container to create the `raw` schema and tables:

```bash
docker exec -i api-postgresql-etl-airflow-postgres psql -U postgres -d fakestore_db < sql/creation.sql
```

#### 4. Access Services & Run Pipeline
- **Airflow Web UI**: Navigate to `http://localhost:8080` in your browser. Log in using the credentials defined in `.env` (default: `airflow` / `airflow`).
- **Trigger DAG**: Unpause and trigger the **`product_etl_pipeline`** DAG to run the automated ETL process.
- **pgAdmin**: Navigate to `http://localhost:5050` to inspect database tables visually.

To stop the services:
```bash
docker compose down
```

---

### Option 2: Local Python Setup

Run the ETL pipeline directly on your local machine using Python and a local PostgreSQL instance.

#### Prerequisites
- **Python**: `3.12` or higher
- **PostgreSQL**: Running PostgreSQL instance

#### 1. Installation

```bash
# Clone the repository
git clone https://github.com/mohamedhaitham22/api-postgresql-etl.git
cd api-postgresql-etl

# Create virtual environment
python -m venv .etl-venv

# Activate virtual environment
# Windows PowerShell:
.\.etl-venv\Scripts\Activate.ps1
# Linux/macOS:
source .etl-venv/bin/activate

# Install dependencies in editable mode
pip install -e .
```

#### 2. Environment Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Set your local PostgreSQL connection settings in `.env`.

#### 3. Database Initialization

Execute [`sql/creation.sql`] in PostgreSQL to create the `raw` schema and tables:

```bash
psql -h localhost -U postgres -d fakestore_db -f sql/creation.sql
```

#### 4. Running the Pipeline

Execute the pipeline directly:

```bash
python -m src.main
```

---

## 📊 Analytics & Verification

After running the pipeline, execute analytical queries from [`sql/analytics_queries.sql`]:

```bash
psql -h localhost -U postgres -d fakestore_db -f sql/analytics_queries.sql
```

Sample queries included:
- Product prices ordered descending
- Average product price & count per category
- Stock alerts (products with stock < 20)
- High discount products (>= 20%)
- Review statistics and ratings aggregations
