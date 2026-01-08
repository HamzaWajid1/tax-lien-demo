-- Properties table
CREATE TABLE properties (
    property_id SERIAL PRIMARY KEY,
    business_name VARCHAR(255) NOT NULL,
    owner_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    county VARCHAR(100) NOT NULL,
    state VARCHAR(20) DEFAULT 'FL'
);

-- Tax Liens table
CREATE TABLE tax_liens (
    certificate_number VARCHAR(50) PRIMARY KEY,
    property_id INT REFERENCES properties(property_id),
    face_amount NUMERIC NOT NULL
);
