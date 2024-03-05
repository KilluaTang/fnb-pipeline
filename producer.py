import csv
import json
import logging
import requests

from io import BytesIO
from avro.datafile import DataFileWriter
from avro.io import DatumWriter
from avro.schema import parse as avro_parse
from avro.schema import PrimitiveSchema as avro_primitive_schema
from confluent_kafka import Producer

from config import avro_schemas

logger = logging.getLogger(__name__)

class KafkaProducerWrapper:
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.producer = Producer({'bootstrap.servers': self.bootstrap_servers})

    def produce_csv_data(self, url, topic):
        response = requests.get(url)
        response.raise_for_status()
        csv_data = response.text.splitlines()

        logger.info(f"Producing messages to topic {topic}")

        schema = avro_parse(json.dumps(avro_schemas[topic]['schema']))  # Parse schema from JSON string

        reader = csv.DictReader(csv_data)
        for row in reader:
            # Convert data types based on schema
            converted_row = {}
            for field in schema.fields:  # Access fields using schema.fields
                field_name = field.name
                field_type = field.type

                # Get the value from the CSV row
                value = row.get(field_name)

                # Convert the value to the appropriate type
                if isinstance(field_type, avro_primitive_schema):
                    if field_type.type == 'int':
                        converted_value = int(value) if value else 0
                    elif field_type.type == 'float':
                        converted_value = float(value) if value else 0
                    elif field_type.type == 'boolean':
                        converted_value = value.lower() in ('true', 't', '1') if value else False
                    else:
                        converted_value = value
                else:
                    converted_value = value

                converted_row[field_name] = converted_value

            # Serialize the converted row using Avro
            writer = DataFileWriter(BytesIO(), DatumWriter(), schema)
            writer.append(converted_row)
            writer.flush()  # Flush the writer's buffer
            serialized_data = writer.writer.getvalue()  # Get the serialized data

            # Produce the serialized row as a message to Kafka
            self.producer.produce(topic=topic, value=serialized_data)
            # logger.info(f"Produced message to topic {topic}: {serialized_data}")

            # Reset the buffer for the next row
            writer = None

        self.producer.flush()
