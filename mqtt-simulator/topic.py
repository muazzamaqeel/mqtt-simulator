# topic.py
import random
import time
import json
import threading
import paho.mqtt.client as mqtt
from data_classes import BrokerSettings, ClientSettings
from topic_data import TopicDataNumber, TopicDataBool, TopicDataRawValue, TopicDataMathExpression

class Topic(threading.Thread):
    def __init__(self, broker_settings: BrokerSettings, topic_url: str, topic_data: list[object], topic_payload_root: object, client_settings: ClientSettings):
        threading.Thread.__init__(self)
        self.broker_settings = broker_settings
        self.topic_url = topic_url
        self.topic_data = self.load_topic_data(topic_data)
        self.topic_payload_root = topic_payload_root
        self.client_settings = client_settings
        self.loop = False
        self.client = None
        self.payload = None

    def load_topic_data(self, topic_data_object):
        topic_data = []
        for data in topic_data_object:
            data_type = data['TYPE']
            if data_type == 'int' or data_type == 'float':
                topic_data.append(TopicDataNumber(data))
            elif data_type == 'bool':
                topic_data.append(TopicDataBool(data))
            elif data_type == 'raw_values':
                topic_data.append(TopicDataRawValue(data))
            elif data_type == 'math_expression':
                topic_data.append(TopicDataMathExpression(data))
            else:
                raise NameError(f"Data TYPE '{data_type}' is unknown")
        return topic_data

    def connect(self):
        self.loop = True
        clean_session = None if self.broker_settings.protocol == mqtt.MQTTv5 else self.client_settings.clean
        self.client = mqtt.Client(self.topic_url, protocol=self.broker_settings.protocol, clean_session=clean_session)
        self.client.on_publish = self.on_publish
        self.client.connect(self.broker_settings.url, self.broker_settings.port)
        self.client.loop_start()

    def disconnect(self):
        self.loop = False
        self.client.loop_stop()
        self.client.disconnect()

    def run(self):
        self.connect()
        while self.loop:
            try:
                self.payload = self.generate_payload()
                self.client.publish(topic=self.topic_url, payload=json.dumps(self.payload), qos=self.client_settings.qos, retain=self.client_settings.retain)
            except (mqtt.MQTTException, ConnectionError) as e:
                print(f"Connection error on topic {self.topic_url}: {e}. Attempting to reconnect...")
                time.sleep(5)
                self.connect()  # Try to reconnect
            time.sleep(self.client_settings.time_interval)

    def on_publish(self, client, userdata, result):
        payload_str = ', '.join(f"{key}={value}" for key, value in self.payload.items())
        print(f'[{time.strftime("%H:%M:%S")}] Data published on: {self.topic_url} {payload_str}')

    def generate_payload(self):
        payload = {}
        payload.update(self.topic_payload_root)
        has_data_active = False

        # Populate payload based on topic type
        if "ppg" in self.topic_url:
            # Pacifier fields for 'ppg' sensor type
            payload["led1"] = random.randint(100, 110)  # Simulate LED values within a specific range
            payload["led2"] = random.randint(100, 110)
            payload["led3"] = random.randint(100, 110)
            payload["temperature"] = round(random.uniform(36.5, 37.5), 1)  # Example temperature range

        elif "imu" in self.topic_url:
            # Pacifier fields for 'imu' sensor type with only accelerometer, gyroscope, and magnetometer
            payload["acc_x"] = round(random.uniform(-0.03, 0.03), 2)
            payload["acc_y"] = round(random.uniform(-0.03, 0.03), 2)
            payload["acc_z"] = round(random.uniform(-0.03, 0.03), 2)
            payload["gyro_x"] = round(random.uniform(-0.2, 0.2), 2)
            payload["gyro_y"] = round(random.uniform(-0.2, 0.2), 2)
            payload["gyro_z"] = round(random.uniform(-0.2, 0.2), 2)
            payload["mag_x"] = round(random.uniform(-0.05, 0.05), 2)
            payload["mag_y"] = round(random.uniform(-0.05, 0.05), 2)
            payload["mag_z"] = round(random.uniform(-0.05, 0.05), 2)

        has_data_active = True
        return payload if has_data_active else None

