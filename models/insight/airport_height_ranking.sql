{{
    config(
        enabled=true,
        materialized='table',
    )
}}
-- Which are the highest and lowest elevated airports, airfields and heliports on the planet? 
WITH ranked_airports AS (
    SELECT 
        a.type,
        a.name,
        a.elevation_ft,
        a.iso_country,
        a.iso_region,
        ROW_NUMBER() OVER (PARTITION BY a.type ORDER BY a.elevation_ft DESC) AS highest_rank,
        ROW_NUMBER() OVER (PARTITION BY a.type ORDER BY a.elevation_ft ASC) AS lowest_rank
    FROM 
        {{source('ourairports','airports')}} a
    JOIN 
        {{source('ourairports','countries')}} c ON a.iso_country = c.code
    WHERE 
        a.elevation_ft IS NOT NULL
        AND a.type != 'closed'
)
SELECT 
    ra.type,
    ra.name,
    ra.elevation_ft,
    c.name AS country_name,
    ra.iso_region
FROM 
    ranked_airports ra
JOIN 
    {{source('ourairports','countries')}} c ON ra.iso_country = c.code
WHERE 
    (highest_rank = 1 OR lowest_rank = 1)
ORDER BY 
    ra.type, ra.elevation_ft
