import json

from kafka import KafkaProducer, KafkaConsumer
import logging


class KafkaProducerService:
    def __init__(self, servers=None):
        if servers is None:
            servers = ['localhost:9092', ]

        _producer = None
        try:
            _producer = KafkaProducer(bootstrap_servers=servers, api_version=(0, 10))
        except Exception as ex:
            logging.error(f'Exception while connecting Kafka, err = {ex}')
        finally:
            self.producer = _producer

    def publish_message(self, topic_name, key, value):
        try:
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            self.producer.send(topic_name, key=key_bytes, value=value_bytes)
        except Exception as e:
            logging.error(f"Error at publishing message on topic {topic_name}, err = {e}")


class KafkaConsumerService:
    def __init__(self):
        pass

    def read_messages(self, topic, servers=None):
        if servers is None:
            servers = ['localhost:9092', ]

        consumer = KafkaConsumer(topic, bootstrap_servers=servers,
                                 auto_offset_reset='earliest',
                                 api_version=(0, 10),
                                 consumer_timeout_ms=1000)

        messages = []
        for msg in consumer:
            key = msg.key.decode('utf-8')
            value = json.loads(msg.value.decode('utf-8'))
            messages.append(value)

        if consumer is not None:
            consumer.close()

        return messages
