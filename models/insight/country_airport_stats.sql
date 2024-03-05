{{
    config(
        enabled=true,
        materialized='table',
    )
}}
-- How many airports, airfields and heliports exist in each country and continent? 
-- What is the average elevation of the airports, airfields and heliports in each country?
-- How many cities/towns/settlements in each country?
-- What is the min, max and average elevation of the cities per country?
SELECT 
    c.name AS country_name,
    c.continent AS continent,
    COUNT(a.id) AS total_airports,
    COUNT(DISTINCT a.municipality) AS number_of_cities,
    MIN(a.elevation_ft) AS min_city_elevation,
    MAX(a.elevation_ft) AS max_city_elevation,
    AVG(a.elevation_ft) AS avg_city_elevation,
    SUM(CASE WHEN a.type IN ('large_airport', 'medium_airport', 'small_airport', 'seaplane_base', 'balloonport') THEN 1 ELSE 0 END) AS airfields,
    SUM(CASE WHEN a.type = 'heliport' THEN 1 ELSE 0 END) AS heliports,
    AVG(CASE WHEN a.type IN ('large_airport', 'medium_airport', 'small_airport', 'seaplane_base', 'balloonport') THEN a.elevation_ft ELSE NULL END) AS avg_airfield_elevation,
    AVG(CASE WHEN a.type = 'heliport' THEN a.elevation_ft ELSE NULL END) AS avg_heliport_elevation
FROM 
    {{source('ourairports','airports')}} a
JOIN 
    {{source('ourairports','countries')}} c ON a.iso_country = c.code
GROUP BY 
    c.name, c.continent
ORDER BY 
    c.continent, c.name