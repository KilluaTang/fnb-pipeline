import logging
import time

from io import BytesIO
from avro.datafile import DataFileReader
from avro.io import DatumReader
from confluent_kafka import Consumer, KafkaError

from config import avro_schemas
from database import upsert_batch_to_database

logger = logging.getLogger(__name__)

class KafkaConsumerWrapper:
    def __init__(self, bootstrap_servers, group_id, batch_size=100, batch_timeout=60):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.consumer = Consumer({
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest'
        })

    def consume_and_upsert_multiple_topics(self, topics, postgres_db_params):
        self.consumer.subscribe(topics)
        logger.info(f"Consumer subscribed to topics: {topics}")

        try:
            batch = {topic: [] for topic in topics}
            last_batch_time = time.time()
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    if time.time() - last_batch_time > self.batch_timeout:
                        # Timeout reached, upsert the batch
                        for topic, records in batch.items():
                            self._upsert_batch(topic, records, postgres_db_params)
                            batch[topic] = []
                        last_batch_time = time.time()
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        logger.error("Consumer error: {}".format(msg.error()))
                        break

                topic = msg.topic()
                with DataFileReader(BytesIO(msg.value()), DatumReader()) as reader:
                    for record in reader:
                        batch[topic].append(record)
                        if len(batch[topic]) >= self.batch_size:
                            self._upsert_batch(topic, batch[topic], postgres_db_params)
                            batch[topic] = []
                            last_batch_time = time.time()

                # Commit offsets after processing each batch
                self.consumer.commit()

        except KeyboardInterrupt:
            pass

        finally:
            for topic in topics:
                if batch[topic]:
                    self._upsert_batch(topic, batch[topic], postgres_db_params)
            self.consumer.unsubscribe()
            logger.info(f"Consumer unsubscribed from topics: {topics}")
            self.consumer.close()
            logger.info("Consumer closed")

    def _upsert_batch(self, topic, records, postgres_db_params):
        try:
            upsert_batch_to_database(topic, records, avro_schemas[topic]['schema'], postgres_db_params)
        except Exception as e:
            logger.error(f"Error upserting batch for topic {topic}: {e}")
