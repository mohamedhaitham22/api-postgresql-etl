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
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Configuration](#environment-configuration)
  - [Database Initialization](#database-initialization)
  - [Running the Pipeline](#running-the-pipeline)
- [Analytics & Verification](#-analytics--verification)

---

## ✨ Features

- **Extract**: Retrieves batch product data from external REST APIs using a resilient HTTP client (`requests.Session` with timeout and error handling).
- **Raw Persistence**: Saves raw timestamped JSON snapshots under `data/raw/` for auditing and data lineage.
- **Transform**: Normalizes complex nested JSON payloads (dimensions, tags, reviews, metadata, images) into clean relational structures.
- **Load (PostgreSQL)**: Transactionally upserts (`ON CONFLICT DO UPDATE / DO NOTHING`) data into PostgreSQL database tables.
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
- **Database**: PostgreSQL
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
├── pyproject.toml            # Python dependencies and build config
└── README.md                 # Project documentation
```

---

## ⚙️ Getting Started & Setup

### Prerequisites

- **Python**: `3.12` or higher
- **PostgreSQL**: Running PostgreSQL instance

### 1. Installation

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

### 2. Environment Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Set your values in `.env`:
```env
APP_NAME="Fake Store API Pipeline"
APP_ENV="development"

API_BASE_URL="https://dummyjson.com"
API_TIMEOUT=10

POSTGRES_HOST="localhost"
POSTGRES_PORT=5432
POSTGRES_DB="fakestore_db"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="your_password"
POSTGRES_SCHEMA="raw"

RAW_DATA_DIR="data/raw"
PROCESSED_DATA_DIR="data/processed"

LOG_LEVEL="INFO"
LOG_DIRECTORY="logs"
LOG_FILE_NAME="etl.log"
```

### 3. Database Initialization

Execute [`sql/creation.sql`] in PostgreSQL to create the `raw` schema, tables, foreign keys, and indexes:

```bash
psql -h localhost -U postgres -d fakestore_db -f sql/creation.sql
```

### 4. Running the Pipeline

Execute the pipeline:

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
