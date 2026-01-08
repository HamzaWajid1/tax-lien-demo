# 🏛️ Tax Lien Data Engineering Demo – Florida

<div align="center">

**A 48-Hour Challenge Submission for Data Engineer Intern Role at Motate**

*Built by [Hamza Paracha](mailto:hamzaparacha098@gmail.com)*

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue.svg)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-green.svg)](https://www.sqlalchemy.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.1-orange.svg)](https://pandas.pydata.org/)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Database Schema](#-database-schema)
- [ETL Pipeline](#-etl-pipeline)
- [Tech Stack](#-tech-stack)
- [Setup Instructions](#-setup-instructions)
- [Usage](#-usage)
- [Future Improvements](#-future-improvements)
- [Contact](#-contact)

---

## 🎯 Overview

This project is a **48-hour demo submission** for the Data Engineer Intern role at Motate. It demonstrates the ability to:

- ✅ Extract data from Excel files (downloaded from Florida Revenue website)
- ✅ Clean and standardize semi-structured data
- ✅ Design a normalized database schema
- ✅ Build an ETL pipeline using Python, Pandas, and SQLAlchemy
- ✅ Handle data quality issues and duplicates
- ✅ Present end-to-end engineering work

### Selected State: **Florida**

Processes delinquent tax warrant data from the Florida Department of Revenue's publicly available Excel files.

---

## 🏗️ Architecture

### Repository Structure

```
tax-lien-demo/
├── src/
│   ├── scraper.py      # Downloads Excel file from Florida Revenue website
│   └── ETL.py          # Main ETL pipeline script
├── data/
│   └── delinquent_taxes.xlsx  # Source Excel file
├── schema.sql          # Database schema definition
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

### Data Flow

1. **Extract**: `scraper.py` downloads the Excel file from the Florida Revenue website
2. **Transform**: `ETL.py` loads, cleans, and standardizes the data using Pandas
3. **Load**: Data is inserted into PostgreSQL with proper relationships and constraints

---

## 🗄️ Database Schema

**Database Type:** PostgreSQL

### Tables Overview

#### 1. **Properties**
Stores property and owner information with unique address constraint.

| Column | Type | Description |
|--------|------|-------------|
| `property_id` | SERIAL PRIMARY KEY | Unique property identifier |
| `business_name` | VARCHAR(255) NOT NULL | Business name (or "N/A" if not applicable) |
| `owner_name` | VARCHAR(255) NOT NULL | Property owner name |
| `address` | VARCHAR(255) NOT NULL UNIQUE | Property street address (unique constraint) |
| `county` | VARCHAR(100) NOT NULL | County name |
| `state` | VARCHAR(20) DEFAULT 'FL' | State abbreviation (defaults to 'FL') |

#### 2. **Tax Liens**
Core table storing tax lien certificate (warrant) information linked to properties.

| Column | Type | Description |
|--------|------|-------------|
| `certificate_number` | VARCHAR(50) PRIMARY KEY | Tax warrant/certificate number (unique identifier) |
| `property_id` | INT REFERENCES properties(property_id) | Foreign key to properties table |
| `face_amount` | NUMERIC NOT NULL | Original tax amount owed |

### Schema Relationships

- **One-to-Many**: One property can have multiple tax liens
- **Foreign Key**: `tax_liens.property_id` → `properties.property_id`

---

## 🔄 ETL Pipeline

### Extract
- **Source**: Excel file (`delinquent_taxes.xlsx`) downloaded from Florida Revenue website
- **Method**: `scraper.py` uses `requests` and `BeautifulSoup` to find and download the Excel file
- **Script**: `python src/scraper.py`

### Transform
- **Tool**: Pandas for data manipulation
- **Actions Performed**:
  - ✅ Load Excel file with header row (skipping first row)
  - ✅ Rename columns for clarity (`warrant_number`, `warrant_amount`, etc.)
  - ✅ Fill missing business names with "N/A"
  - ✅ Strip whitespace from string columns
  - ✅ Convert `warrant_amount` to numeric (handling errors gracefully)
  - ✅ Remove duplicate warrants based on `warrant_number`
  - ✅ Deduplicate properties based on address

### Load
- **Tool**: SQLAlchemy 2.0 with PostgreSQL
- **Features**:
  - ✅ Creates tables if they don't exist
  - ✅ Adds UNIQUE constraint on `address` column if missing
  - ✅ Uses `ON CONFLICT DO NOTHING` for idempotent inserts
  - ✅ Maps properties to tax liens using foreign key relationships
  - ✅ Handles parameterized queries for security

### ETL Script Execution

```bash
python src/ETL.py
```

The script performs the following steps:
1. Loads Excel data into a Pandas DataFrame
2. Cleans and standardizes the data
3. Connects to PostgreSQL database
4. Creates tables with proper constraints
5. Inserts unique properties (avoiding duplicates by address)
6. Maps property IDs to tax liens
7. Inserts tax lien records (avoiding duplicates by certificate number)

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.11 |
| **Data Processing** | Pandas 2.1.1 |
| **Database** | PostgreSQL 14+ |
| **ORM/DB** | SQLAlchemy 2.0.22 |
| **Database Driver** | psycopg2-binary 2.9.9 |
| **Excel Processing** | openpyxl 3.1.3 |
| **Web Scraping** | requests, BeautifulSoup |
| **NumPy** | 1.25.0 |

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.11+
- PostgreSQL 14+ installed and running
- pip package manager

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/tax-lien-demo.git
cd tax-lien-demo/tax-lien-demo
```

### 2. Create Virtual Environment

It's recommended to use a virtual environment to isolate project dependencies.

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**On Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt when the virtual environment is active.

### 3. Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

**Note**: Keep the virtual environment activated for all subsequent steps. To deactivate it later, simply run `deactivate` in your terminal.

### 4. PostgreSQL Setup

Create the database:

```sql
CREATE DATABASE tax_lien_demo;
```

### 5. Configure Database Connection

Update the `DATABASE_URL` in `src/ETL.py` with your PostgreSQL credentials:

```python
DATABASE_URL = "postgresql://username:password@localhost:5432/tax_lien_demo"
```

**Note**: If your password contains special characters, they should be URL-encoded.

### 6. Download Source Data (Optional)

If you need to download the Excel file:

```bash
python src/scraper.py
```

This will download the Excel file to `data/delinquent_taxes.xlsx`.

### 7. Run ETL Pipeline

```bash
python src/ETL.py
```

The script will:
- Create tables if they don't exist
- Add necessary constraints
- Process and load the data
- Print "ETL completed successfully!" when done

---

## 📊 Usage

### Running the Complete Pipeline

1. **Download the data** (if not already present):
   ```bash
   python src/scraper.py
   ```

2. **Run the ETL process**:
   ```bash
   python src/ETL.py
   ```

### Verifying Results

Query the database to verify data was loaded:

```sql
-- Check property count
SELECT COUNT(*) FROM properties;

-- Check tax lien count
SELECT COUNT(*) FROM tax_liens;

-- View sample data
SELECT p.business_name, p.owner_name, p.address, p.county, 
       tl.certificate_number, tl.face_amount
FROM properties p
JOIN tax_liens tl ON p.property_id = tl.property_id
LIMIT 10;
```

---

## 🔮 Future Improvements

- [ ] Add data validation and quality checks
- [ ] Implement incremental loading (track last processed date)
- [ ] Add error handling and logging
- [ ] Create data quality reports
- [ ] Add unit tests for ETL functions
- [ ] Implement Airflow for scheduling
- [ ] Add Docker containerization
- [ ] Create analytics dashboards (Metabase/Looker)
- [ ] Expand schema to include additional tax lien metadata
- [ ] Add support for multiple data sources

---

## 📝 Technical Notes

### Key Design Decisions

1. **Simplified Schema**: Focused on core entities (properties and tax liens) for the demo
2. **Idempotent Inserts**: Uses `ON CONFLICT DO NOTHING` to allow safe re-runs
3. **Data Cleaning**: Handles missing values, whitespace, and type conversions
4. **Constraint Management**: Automatically adds UNIQUE constraint if missing from existing tables

### Challenges Addressed

- ✅ SQLAlchemy 2.0 parameter passing syntax
- ✅ Handling special characters in database passwords
- ✅ Ensuring UNIQUE constraints exist for ON CONFLICT clauses
- ✅ Excel file path resolution
- ✅ Data type conversions and error handling

---

## 📧 Contact

**Hamza Paracha**

- 📧 Email: [hamzaparacha098@gmail.com](mailto:hamzaparacha098@gmail.com)
- 💼 LinkedIn: *Add your LinkedIn link*

---

<div align="center">

**Made with ❤️ for Motate Data Engineer Intern Challenge**

</div>
