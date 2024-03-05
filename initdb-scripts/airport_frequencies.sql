CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.airport_frequencies (
    id INT PRIMARY KEY,
    airport_ref INT,
    airport_ident VARCHAR,
    type VARCHAR,
    description VARCHAR,
    frequency_mhz DOUBLE PRECISION
);
