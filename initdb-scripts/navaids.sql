CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.navaids (
    id INT PRIMARY KEY,
    filename VARCHAR,
    ident VARCHAR,
    name VARCHAR,
    type VARCHAR,
    frequency_khz INT,
    latitude_deg DOUBLE PRECISION,
    longitude_deg DOUBLE PRECISION,
    elevation_ft INT,
    iso_country VARCHAR,
    dme_frequency_khz INT,
    dme_channel VARCHAR,
    dme_latitude_deg DOUBLE PRECISION,
    dme_longitude_deg DOUBLE PRECISION,
    dme_elevation_ft INT,
    slaved_variation_deg DOUBLE PRECISION,
    magnetic_variation_deg DOUBLE PRECISION,
    usageType VARCHAR,
    power VARCHAR,
    associated_airport VARCHAR
);
