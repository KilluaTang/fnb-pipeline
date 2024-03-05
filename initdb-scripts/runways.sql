CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.runways (
    id INT PRIMARY KEY,
    airport_ref INT,
    airport_ident VARCHAR,
    length_ft INT,
    width_ft INT,
    surface VARCHAR,
    lighted BOOLEAN,
    closed BOOLEAN,
    le_ident VARCHAR,
    le_latitude_deg DOUBLE PRECISION,
    le_longitude_deg DOUBLE PRECISION,
    le_elevation_ft INT,
    le_heading_degT DOUBLE PRECISION,
    le_displaced_threshold_ft INT,
    he_ident VARCHAR,
    he_latitude_deg DOUBLE PRECISION,
    he_longitude_deg DOUBLE PRECISION,
    he_elevation_ft INT,
    he_heading_degT DOUBLE PRECISION,
    he_displaced_threshold_ft INT
);
