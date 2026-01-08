# 🏛️ Tax Lien Data Engineering Demo – Florida

<div align="center">

**A 48-Hour Challenge Submission for Data Engineer Intern Role at Motate**

*Built by [Hamza Paracha](mailto:hamzaparacha098@gmail.com)*

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue.svg)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-green.svg)](https://www.sqlalchemy.org/)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Database Schema](#-database-schema)
- [ETL Pipeline](#-etl-pipeline)
- [Tech Stack](#-tech-stack)
- [Setup Instructions](#-setup-instructions)
- [Sample Output](#-sample-output)
- [Future Improvements](#-future-improvements)
- [Contact](#-contact)

---

## 🎯 Overview

This project is a **48-hour demo submission** for the Data Engineer Intern role at Motate. It showcases the ability to:

- ✅ Design a scalable database schema
- ✅ Build a Python-based web scraping pipeline
- ✅ Clean and standardize semi-structured public data
- ✅ Organize a mini ETL pipeline
- ✅ Present end-to-end engineering work

### Selected State: **Florida**

Structured and publicly accessible tax lien certificate data for demonstration purposes.

---

## 🏗️ Architecture

### Repository Structure

```
tax-lien-demo/
├── src/
│   ├── scraper.py      # Fetches & parses HTML pages
│   ├── parser.py       # Data cleaning/standardization functions
│   ├── db.py           # Database connection (PostgreSQL + SQLAlchemy)
│   └── main.py         # Orchestrates the full pipeline
├── schema.sql          # Full normalized schema
└── README.md           # Documentation
```

---

## 🗄️ Database Schema

**Database Type:** PostgreSQL

### Tables Overview

#### 1. **Properties**
Stores property information with geospatial data.

| Column | Type | Description |
|--------|------|-------------|
| `property_id` | SERIAL PRIMARY KEY | Unique property identifier |
| `parcel_number` | VARCHAR(50) UNIQUE | Parcel identification number |
| `address` | TEXT | Property street address |
| `city` | VARCHAR(100) | City name |
| `county` | VARCHAR(100) | County name |
| `state` | VARCHAR(20) | State abbreviation |
| `zip_code` | VARCHAR(20) | ZIP code |
| `land_use` | VARCHAR(100) | Land use classification |
| `assessed_value` | NUMERIC | Property assessed value |
| `latitude` | FLOAT | Geographic latitude |
| `longitude` | FLOAT | Geographic longitude |

#### 2. **Owners**
Stores property owner information.

| Column | Type | Description |
|--------|------|-------------|
| `owner_id` | SERIAL PRIMARY KEY | Unique owner identifier |
| `owner_name` | VARCHAR(200) | Owner full name |
| `mailing_address` | TEXT | Mailing address |
| `city` | VARCHAR(100) | City name |
| `state` | VARCHAR(20) | State abbreviation |
| `zip_code` | VARCHAR(20) | ZIP code |

#### 3. **Tax Liens**
Core table storing tax lien certificate information.

| Column | Type | Description |
|--------|------|-------------|
| `lien_id` | SERIAL PRIMARY KEY | Unique lien identifier |
| `property_id` | INT | Foreign key → `properties(property_id)` |
| `owner_id` | INT | Foreign key → `owners(owner_id)` |
| `certificate_number` | VARCHAR(50) | Tax lien certificate number |
| `tax_year` | INT | Year of tax assessment |
| `face_amount` | NUMERIC | Original tax amount |
| `interest_rate` | FLOAT | Interest rate (decimal) |
| `status` | VARCHAR(20) | Lien status (e.g., OPEN, REDEEMED) |
| `issue_date` | DATE | Date lien was issued |
| `redeem_by_date` | DATE | Redemption deadline |

#### 4. **Auctions**
Tracks auction information for tax liens.

| Column | Type | Description |
|--------|------|-------------|
| `auction_id` | SERIAL PRIMARY KEY | Unique auction identifier |
| `lien_id` | INT | Foreign key → `tax_liens(lien_id)` |
| `auction_date` | DATE | Date of auction |
| `opening_bid` | NUMERIC | Initial bid amount |
| `winning_bid` | NUMERIC | Final winning bid amount |
| `winning_bidder` | VARCHAR(200) | Name of winning bidder |

#### 5. **Payments**
Records payment transactions for tax liens.

| Column | Type | Description |
|--------|------|-------------|
| `payment_id` | SERIAL PRIMARY KEY | Unique payment identifier |
| `lien_id` | INT | Foreign key → `tax_liens(lien_id)` |
| `payment_date` | DATE | Date of payment |
| `amount_paid` | NUMERIC | Payment amount |
| `payment_method` | VARCHAR(50) | Payment method used |
| `transaction_id` | VARCHAR(100) | Transaction identifier |

---

## 🔄 ETL Pipeline

### Extract
- **Description:** Load tax lien listing pages and extract certificate info, parcel numbers, face amount, interest rate, owner names, etc.
- **Libraries:** `requests`, `BeautifulSoup`
- **Features:**
  - ✅ Handles pagination
  - ✅ Fetches multiple pages

### Transform
- **Description:** Standardize and clean extracted fields
- **Actions:**
  - 🔄 Currency to float conversion
  - 🔄 Percentage to decimal conversion
  - 🔄 Dates to ISO format
  - 🔄 Deduplication by `parcel_number` and `tax_year`

### Load
- **Description:** Load cleaned data into PostgreSQL using SQLAlchemy
- **Features:**
  - ✅ Foreign key relationships
  - ✅ Modular design for production

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.10 |
| **Web Scraping** | `requests`, `BeautifulSoup` |
| **Database** | PostgreSQL 14 |
| **ORM** | SQLAlchemy |
| **Data Cleaning** | Custom Python utilities |
| **Tools** | Git, VS Code, ChatGPT (boilerplate assistance) |

---

## 🚀 Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/tax-lien-demo.git
cd tax-lien-demo
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. PostgreSQL Setup

```sql
CREATE DATABASE tax_lien_demo;
```

Update `DATABASE_URL` in `db.py` if necessary.

### 4. Apply Schema

```bash
psql -d tax_lien_demo -f schema.sql
```

### 5. Run Pipeline

```bash
python src/main.py
```

---

## 📊 Sample Output

### Example Record

```json
{
  "certificate_number": "12345",
  "parcel_number": "02-4003-345-0010",
  "tax_year": 2023,
  "face_amount": 450.12,
  "interest_rate": 0.18,
  "status": "OPEN"
}
```

---

## 🎥 Video Demo

**Duration:** 3-5 minutes  
**Link:** *Add your Loom/YouTube link here*

**Contents:**
- 📐 Schema design explanation
- 🏗️ Pipeline architecture
- 💻 Code walkthrough
- 📈 Output results

---

## 🔮 Future Improvements

- [ ] Add Airflow for scheduling
- [ ] Add retry logic and rotating proxies
- [ ] Create analytics dashboards (Metabase/Looker)
- [ ] Add county-level ingest modularization
- [ ] Add Docker containerization

---

## 📝 AI Assistance Note

ChatGPT was used to accelerate:
- Repo structure planning
- Boilerplate code
- README formatting
- Video demo script

**All architectural decisions, data modeling, debugging, and pipeline integration were done manually.**

**Time Invested:** Approximately 7 hours across 48 hours

---

## 📧 Contact

**Hamza Paracha**

- 📧 Email: [hamzaparacha098@gmail.com](mailto:hamzaparacha098@gmail.com)
- 💼 LinkedIn: *Add your LinkedIn link*

---

<div align="center">

**Made with ❤️ for Motate Data Engineer Intern Challenge**

</div>
