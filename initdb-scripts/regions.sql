CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.regions (
    id INT PRIMARY KEY,
    code VARCHAR,
    local_code VARCHAR,
    name VARCHAR,
    continent VARCHAR,
    iso_country VARCHAR,
    wikipedia_link VARCHAR,
    keywords VARCHAR
);
