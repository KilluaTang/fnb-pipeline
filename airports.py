import logging

from producer import KafkaProducerWrapper
from consumer import KafkaConsumerWrapper
from config import kafka_bootstrap_servers, postgres_db_params, csv_data, world_population_url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    producer = KafkaProducerWrapper(kafka_bootstrap_servers)
    consumer = KafkaConsumerWrapper(kafka_bootstrap_servers, group_id='fnb_group')

    for data in csv_data:
        logger.info(f"Processing data for topic: {data['topic']}")
        producer.produce_csv_data(data['url'], data['topic'])

    topics_to_consume = [data['topic'] for data in csv_data]
    consumer.consume_and_upsert_multiple_topics(topics_to_consume, postgres_db_params)

if __name__ == "__main__":
    main()
