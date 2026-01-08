project:
  name: "Tax Lien Data Engineering Demo – Florida"
  role: "Motate – Data Engineer Intern (48-Hour Challenge)"
  author: "Hamza Paracha"
overview:
  description: |
    This project is a 48-hour demo submission for the Data Engineer Intern role at Motate.
    It showcases the ability to design a scalable database schema, build a Python-based web scraping pipeline,
    clean and standardize semi-structured public data, organize a mini ETL pipeline, and present end-to-end engineering work.
  selected_state: "Florida"
  reason: "Structured and publicly accessible tax lien certificate data for demonstration purposes."
architecture:
  repo_structure:
    tax-lien-demo/:
      src/:
        - scraper.py: "Fetches & parses HTML pages"
        - parser.py: "Data cleaning/standardization functions"
        - db.py: "Database connection (PostgreSQL + SQLAlchemy)"
        - main.py: "Orchestrates the full pipeline"
      - schema.sql: "Full normalized schema"
      - README.md: "Documentation"
database_schema:
  type: "PostgreSQL"
  tables:
    properties:
      columns:
        - property_id: "SERIAL PRIMARY KEY"
        - parcel_number: "VARCHAR(50) UNIQUE"
        - address: "TEXT"
        - city: "VARCHAR(100)"
        - county: "VARCHAR(100)"
        - state: "VARCHAR(20)"
        - zip_code: "VARCHAR(20)"
        - land_use: "VARCHAR(100)"
        - assessed_value: "NUMERIC"
        - latitude: "FLOAT"
        - longitude: "FLOAT"
    owners:
      columns:
        - owner_id: "SERIAL PRIMARY KEY"
        - owner_name: "VARCHAR(200)"
        - mailing_address: "TEXT"
        - city: "VARCHAR(100)"
        - state: "VARCHAR(20)"
        - zip_code: "VARCHAR(20)"
    tax_liens:
      columns:
        - lien_id: "SERIAL PRIMARY KEY"
        - property_id: "INT REFERENCES properties(property_id)"
        - owner_id: "INT REFERENCES owners(owner_id)"
        - certificate_number: "VARCHAR(50)"
        - tax_year: "INT"
        - face_amount: "NUMERIC"
        - interest_rate: "FLOAT"
        - status: "VARCHAR(20)"
        - issue_date: "DATE"
        - redeem_by_date: "DATE"
    auctions:
      columns:
        - auction_id: "SERIAL PRIMARY KEY"
        - lien_id: "INT REFERENCES tax_liens(lien_id)"
        - auction_date: "DATE"
        - opening_bid: "NUMERIC"
        - winning_bid: "NUMERIC"
        - winning_bidder: "VARCHAR(200)"
    payments:
      columns:
        - payment_id: "SERIAL PRIMARY KEY"
        - lien_id: "INT REFERENCES tax_liens(lien_id)"
        - payment_date: "DATE"
        - amount_paid: "NUMERIC"
        - payment_method: "VARCHAR(50)"
        - transaction_id: "VARCHAR(100)"
etl_pipeline:
  extract:
    description: "Load tax lien listing pages and extract certificate info, parcel numbers, face amount, interest rate, owner names, etc."
    libraries: ["requests", "BeautifulSoup"]
    features: ["Handles pagination", "Fetch multiple pages"]
  transform:
    description: "Standardize and clean extracted fields"
    actions:
      - currency_to_float
      - percentage_to_decimal
      - dates_to_ISO
      - deduplicate_by: ["parcel_number", "tax_year"]
  load:
    description: "Load cleaned data into PostgreSQL using SQLAlchemy"
    features: ["Foreign key relationships", "Modular design for production"]
tech_stack:
  language: "Python 3.10"
  web_scraping: ["requests", "BeautifulSoup"]
  database: "PostgreSQL 14"
  orm: "SQLAlchemy"
  data_cleaning: "Custom Python utilities"
  tools: ["Git", "VS Code", "ChatGPT (boilerplate assistance)"]
setup_instructions:
  clone_repo: |
    git clone https://github.com/<your-username>/tax-lien-demo.git
    cd tax-lien-demo
  install_dependencies: "pip install -r requirements.txt"
  postgresql_setup:
    create_db: "CREATE DATABASE tax_lien_demo;"
    update_credentials: "Update DATABASE_URL in db.py if necessary"
  apply_schema: "psql -d tax_lien_demo -f schema.sql"
  run_pipeline: "python src/main.py"
sample_output:
  example_record:
    certificate_number: "12345"
    parcel_number: "02-4003-345-0010"
    tax_year: 2023
    face_amount: 450.12
    interest_rate: 0.18
    status: "OPEN"
ai_assistance:
  description: "ChatGPT was used to accelerate repo structure planning, boilerplate code, README formatting, and video demo script."
  manual_work: "All architectural decisions, data modeling, debugging, and pipeline integration were done manually."
time_invested: "Approximately 7 hours across 48 hours"
video_demo:
  duration: "3-5 minutes"
  link: "Add your Loom/YouTube link here"
  contents:
    - "Schema design explanation"
    - "Pipeline architecture"
    - "Code walkthrough"
    - "Output results"
future_improvements:
  - "Add Airflow for scheduling"
  - "Add retry logic and rotating proxies"
  - "Create analytics dashboards (Metabase/Looker)"
  - "Add county-level ingest modularization"
  - "Add Docker containerization"
contact:
  name: "Hamza Paracha"
  email: "hamzaparacha098@gmail.com"
  linkedin: "Add your LinkedIn link"
