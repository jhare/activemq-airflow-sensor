from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
import pika

class ActiveMQSensor(BaseSensorOperator):
    @apply_defaults
    def __init__(self, message_count_check_method, *args, **kwargs):
        super(ActiveMQSensor, self).__init__(*args, **kwargs)
        self.message_count_check_method = message_count_check_method

    def poke(self, context):
        with pika.BlockingConnection(pika.ConnectionParameters('localhost')) as connection:
            channel = connection.channel()
            channel.queue_declare(queue=self.queue)
            channel.basic_consume(queue=self.queue, on_message_callback=self.message_count_check_method)
            channel.start_consuming()

    def message_count_check_method(self, channel, method, properties, body):
        self.log.info("Received message count: %s", body)
        self.set_poke_interval(self.poke_interval)
