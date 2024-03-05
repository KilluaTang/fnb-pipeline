CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.countries (
    id INT PRIMARY KEY,
    code VARCHAR,
    name VARCHAR,
    continent VARCHAR,
    wikipedia_link TEXT,
    keywords VARCHAR
);
