CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.country_population (
    id SERIAL PRIMARY KEY,
    country_name TEXT,
    population BIGINT
);