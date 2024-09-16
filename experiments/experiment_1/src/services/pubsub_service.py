from google import pubsub_v1

from experiments.experiment_1.src.constants import PUBSUB_TOPIC, PUBSUB_PROJECT_ID


class PubSubService:
    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(PUBSUB_PROJECT_ID, PUBSUB_TOPIC)

    def publish_message(self, message):
        try:
            future = self.publisher.publish(topic=self.topic_path, messages=message.encode('utf-8'))
            future.result()
            print(f"Message published to Pub/Sub: {message}")
        except Exception as e:
            print(f"Error publishing message to Pub/Sub: {e}")
