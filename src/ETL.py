import pandas as pd
from sqlalchemy import create_engine, text

# -------------------------------
# CONFIGURATION
# -------------------------------

# Path to Excel file
excel_file = "../tax-lien-demo/data/delinquent_taxes.xlsx"

# PostgreSQL connection string
DATABASE_URL = "postgresql://postgres:Hamza.paracha1@localhost:5432/tax_lien_demo"

# -------------------------------
# STEP 1: LOAD EXCEL
# -------------------------------

df = pd.read_excel(excel_file, header=1)

# Rename columns for clarity
df.columns = [
    "business_name",
    "owner_name",
    "address",
    "county",
    "warrant_number",
    "warrant_amount"
]

# -------------------------------
# STEP 2: CLEAN DATA
# -------------------------------

# Fill missing business names
df['business_name'] = df['business_name'].fillna("N/A")

# Strip whitespace from string columns
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Convert warrant_amount to numeric
df['warrant_amount'] = pd.to_numeric(df['warrant_amount'], errors='coerce')

# Drop duplicate warrants
df = df.drop_duplicates(subset=['warrant_number'])

# -------------------------------
# STEP 3: CONNECT TO DATABASE
# -------------------------------

engine = create_engine(DATABASE_URL)

# -------------------------------
# STEP 4: CREATE TABLES IF NOT EXISTS
# -------------------------------

with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS properties (
            property_id SERIAL PRIMARY KEY,
            business_name VARCHAR(255) NOT NULL,
            owner_name VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL,
            county VARCHAR(100) NOT NULL,
            state VARCHAR(20) DEFAULT 'FL'
        );
    """))

    # Add UNIQUE constraint on address if it doesn't exist
    conn.execute(text("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint 
                WHERE conname = 'properties_address_key'
            ) THEN
                ALTER TABLE properties ADD CONSTRAINT properties_address_key UNIQUE (address);
            END IF;
        END $$;
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS tax_liens (
            certificate_number VARCHAR(50) PRIMARY KEY,
            property_id INT REFERENCES properties(property_id),
            face_amount NUMERIC NOT NULL
        );
    """))

# -------------------------------
# STEP 5: INSERT PROPERTIES
# -------------------------------

properties_df = df[['business_name', 'owner_name', 'address', 'county']].drop_duplicates()
properties_df['state'] = 'FL'

with engine.begin() as conn:
    for _, row in properties_df.iterrows():
        conn.execute(
            text("""
                INSERT INTO properties (business_name, owner_name, address, county, state)
                VALUES (:business_name, :owner_name, :address, :county, :state)
                ON CONFLICT (address) DO NOTHING
            """),
            parameters=row.to_dict()
        )

# -------------------------------
# STEP 6: MAP property_id
# -------------------------------

properties_db = pd.read_sql("SELECT property_id, address FROM properties", engine)
df = df.merge(properties_db, on='address', how='left')

# -------------------------------
# STEP 7: INSERT TAX LIENS
# -------------------------------

tax_liens_df = df[['warrant_number', 'property_id', 'warrant_amount']].rename(
    columns={'warrant_number': 'certificate_number', 'warrant_amount': 'face_amount'}
)

with engine.begin() as conn:
    for _, row in tax_liens_df.iterrows():
        conn.execute(
            text("""
                INSERT INTO tax_liens (certificate_number, property_id, face_amount)
                VALUES (:certificate_number, :property_id, :face_amount)
                ON CONFLICT (certificate_number) DO NOTHING
            """),
            parameters=row.to_dict()
        )

print("ETL completed successfully!")

