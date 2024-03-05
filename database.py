import logging
import psycopg2
from psycopg2 import sql

logger = logging.getLogger(__name__)

def upsert_batch_to_database(table_name, batch, schema, postgres_db_params):
    conn = None
    try:
        # Connect to the PostgreSQL database using the parameters from config.py
        conn = psycopg2.connect(**postgres_db_params)
        cur = conn.cursor()

        # Extract fields from the Avro schema
        fields = schema['fields']
        field_names = [field['name'] for field in fields]

        # Define the SQL upsert query dynamically based on the schema
        table_name = table_name.replace('-', '_')
        columns = ', '.join(field_names)  # Include all fields from the schema
        placeholders = ', '.join(['%s'] * len(field_names))
        upsert_query = f"""
            INSERT INTO raw.{table_name} ({columns})
            VALUES ({placeholders})
            ON CONFLICT (id) DO UPDATE
            SET {', '.join([f"{field} = EXCLUDED.{field}" for field in field_names])}
        """

        # Extract message values based on schema for all records in the batch
        batch_values = [[record.get(field['name']) for field in fields] for record in batch]

        # Execute the upsert query for the entire batch
        for batch_value in batch_values:
            cur.execute(upsert_query, batch_value)

        # Commit the transaction
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error upserting batch for table {table_name}: {error}")

    finally:
        if conn is not None:
            # Close database connection
            conn.close()

def truncate_and_insert_to_database(table_name, data, schema, postgres_db_params):
    conn = None
    try:
        # Connect to the PostgreSQL database using the parameters from config.py
        conn = psycopg2.connect(**postgres_db_params)
        cur = conn.cursor()

        # Truncate the table
        cur.execute(sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY").format(sql.Identifier('raw', table_name)))

        # Extract fields from the Avro schema
        fields = schema['fields']
        field_names = [field['name'] for field in fields]

        # Define the SQL insert query dynamically based on the schema
        columns = ', '.join(field_names)  # Include all fields from the schema
        placeholders = ', '.join(['%s'] * len(field_names))
        insert_query = f"""
            INSERT INTO raw.{table_name} ({columns})
            VALUES ({placeholders})
        """

        # Extract values from the data
        data_values = [[record[field['name']] for field in fields] for record in data]

        # Execute the insert query for all records
        cur.executemany(insert_query, data_values)

        # Commit the transaction
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error truncating and inserting data into table {table_name}: {error}")

    finally:
        if conn is not None:
            # Close database connection
            conn.close()

