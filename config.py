# Kafka bootstrap server
kafka_bootstrap_servers = "kafka-broker-1:9092"
# PostgreSQL database parameters
postgres_db_params = {
    'dbname': 'fnb_demo',
    'user': 'fnb',
    'password': 'S3cret',
    'host': 'postgres'
}

# World population url
world_population_url = "https://www.worldometers.info/world-population/population-by-country/"

# Avro schemas for each topic
avro_schemas = {
    'airports': {
        'schema': {
            'type': 'record',
            'name': 'Airport',
            'fields': [
                {'name': 'id', 'type': 'int'},
                {'name': 'ident', 'type': 'string'},
                {'name': 'type', 'type': 'string'},
                {'name': 'name', 'type': 'string'},
                {'name': 'latitude_deg', 'type': 'float'},
                {'name': 'longitude_deg', 'type': 'float'},
                {'name': 'elevation_ft', 'type': 'int'},
                {'name': 'continent', 'type': 'string'},
                {'name': 'iso_country', 'type': 'string'},
                {'name': 'iso_region', 'type': 'string'},
                {'name': 'municipality', 'type': 'string'},
                {'name': 'scheduled_service', 'type': 'string'},
                {'name': 'gps_code', 'type': 'string'},
                {'name': 'iata_code', 'type': 'string'},
                {'name': 'local_code', 'type': 'string'},
                {'name': 'home_link', 'type': 'string'},
                {'name': 'wikipedia_link', 'type': 'string'},
                {'name': 'keywords', 'type': 'string'}
            ]
        }
    },
    'airport-frequencies': {
        'schema': {
            'type': 'record',
            'name': 'AirportFrequency',
            'fields': [
                {'name': 'id', 'type': 'int'},
                {'name': 'airport_ref', 'type': 'int'},
                {'name': 'airport_ident', 'type': 'string'},
                {'name': 'type', 'type': 'string'},
                {'name': 'description', 'type': 'string'},
                {'name': 'frequency_mhz', 'type': 'float'}
            ]
        }
    },
    'runways': {
        'schema': {
            'type': 'record',
            'name': 'Runways',
            'fields': [
                {'name': 'id', 'type': 'int'},
                {'name': 'airport_ref', 'type': 'int'},
                {'name': 'airport_ident', 'type': 'string'},
                {'name': 'length_ft', 'type': 'int'},
                {'name': 'width_ft', 'type': 'int'},
                {'name': 'surface', 'type': 'string'},
                {'name': 'lighted', 'type': 'boolean'},
                {'name': 'closed', 'type': 'boolean'},
                {'name': 'le_ident', 'type': 'string'},
                {'name': 'le_latitude_deg', 'type': 'float'},
                {'name': 'le_longitude_deg', 'type': 'float'},
                {'name': 'le_elevation_ft', 'type': 'int'},
                {'name': 'le_heading_degT', 'type': 'float'},
                {'name': 'le_displaced_threshold_ft', 'type': 'int'},
                {'name': 'he_ident', 'type': 'string'},
                {'name': 'he_latitude_deg', 'type': 'float'},
                {'name': 'he_longitude_deg', 'type': 'float'},
                {'name': 'he_elevation_ft', 'type': 'int'},
                {'name': 'he_heading_degT', 'type': 'float'},
                {'name': 'he_displaced_threshold_ft', 'type': 'int'}
            ]
        }
    },
    'navaids': {
        'schema': {
            'type': 'record',
            'name': 'Navaids',
            'fields': [
                {'name': 'id', 'type': 'int'},
                {'name': 'filename', 'type': 'string'},
                {'name': 'ident', 'type': 'string'},
                {'name': 'name', 'type': 'string'},
                {'name': 'type', 'type': 'string'},
                {'name': 'frequency_khz', 'type': 'int'},
                {'name': 'latitude_deg', 'type': 'float'},
                {'name': 'longitude_deg', 'type': 'float'},
                {'name': 'elevation_ft', 'type': 'int'},
                {'name': 'iso_country', 'type': 'string'},
                {'name': 'dme_frequency_khz', 'type': 'int'},
                {'name': 'dme_channel', 'type': 'string'},
                {'name': 'dme_latitude_deg', 'type': 'float'},
                {'name': 'dme_longitude_deg', 'type': 'float'},
                {'name': 'dme_elevation_ft', 'type': 'int'},
                {'name': 'slaved_variation_deg', 'type': 'float'},
                {'name': 'magnetic_variation_deg', 'type': 'float'},
                {'name': 'usageType', 'type': 'string'},
                {'name': 'power', 'type': 'string'},
                {'name': 'associated_airport', 'type': 'string'}
            ]
        }
    },
    'regions': {
        'schema': {
            'type': 'record',
            'name': 'Regions',
            'fields': [
                {'name': 'id', 'type': 'int'},
                {'name': 'code', 'type': 'string'},
                {'name': 'local_code', 'type': 'string'},
                {'name': 'name', 'type': 'string'},
                {'name': 'continent', 'type': 'string'},
                {'name': 'iso_country', 'type': 'string'},
                {'name': 'wikipedia_link', 'type': 'string'},
                {'name': 'keywords', 'type': 'string'}
            ]
        }
    },
    'countries': {
        'schema': {
            'type': 'record',
            'name': 'Regions',
            'fields': [
                {'name': 'id', 'type': 'int'},
                {'name': 'code', 'type': 'string'},
                {'name': 'name', 'type': 'string'},
                {'name': 'continent', 'type': 'string'},
                {'name': 'wikipedia_link', 'type': 'string'},
                {'name': 'keywords', 'type': 'string'}
            ]
        }
    }
}

# CSV data to be consumed and produced
csv_data = [
    {
        'url': 'https://davidmegginson.github.io/ourairports-data/airports.csv',
        'topic': 'airports',
        'schema': avro_schemas['airports']['schema']
    },
    {
        'url': 'https://davidmegginson.github.io/ourairports-data/airport-frequencies.csv',
        'topic': 'airport-frequencies',
        'schema': avro_schemas['airport-frequencies']['schema']
    },
    {
        'url': 'https://davidmegginson.github.io/ourairports-data/runways.csv',
        'topic': 'runways',
        'schema': avro_schemas['runways']['schema']
    },
    {
        'url': 'https://davidmegginson.github.io/ourairports-data/navaids.csv',
        'topic': 'navaids',
        'schema': avro_schemas['navaids']['schema']
    },
    {
        'url': 'https://davidmegginson.github.io/ourairports-data/regions.csv',
        'topic': 'regions',
        'schema': avro_schemas['regions']['schema']
    },
    {
        'url': 'https://davidmegginson.github.io/ourairports-data/countries.csv',
        'topic': 'countries',
        'schema': avro_schemas['countries']['schema']
    }
]