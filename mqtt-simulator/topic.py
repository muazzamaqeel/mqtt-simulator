import random
import time
import threading
import struct
import sensor_data_pb2  # Import the compiled Protobuf definitions
import paho.mqtt.client as mqtt
from data_classes import BrokerSettings, ClientSettings
from topic_data import TopicDataNumber, TopicDataBool, TopicDataRawValue, TopicDataMathExpression

class Topic(threading.Thread):
    def __init__(self, broker_settings: BrokerSettings, topic_url: str, topic_data: list, topic_payload_root: dict, client_settings: ClientSettings):
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
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()

    def run(self):
        self.connect()
        while self.loop:
            try:
                # Generate Protobuf payload and publish it
                self.payload = self.generate_protobuf_payload()
                self.client.publish(topic=self.topic_url, payload=self.payload, qos=self.client_settings.qos, retain=self.client_settings.retain)
                
                # Delay between publishes based on time_interval
                time.sleep(self.client_settings.time_interval)

            except (mqtt.MQTTException, ConnectionError) as e:
                print(f"Connection error on topic {self.topic_url}: {e}. Attempting to reconnect...")
                time.sleep(5)
                self.connect()

    def on_publish(self, client, userdata, result):
        payload_str = ', '.join(f"{key}={value}" for key, value in self.payload_readable.items())
        print(f"[{time.strftime('%H:%M:%S')}] Data published on: {self.topic_url} {payload_str}")


    def generate_protobuf_payload(self):
        # Create a SensorData Protobuf message
        sensor_data = sensor_data_pb2.SensorData()
        sensor_data.pacifier_id = self.extract_pacifier_id(self.topic_url)
        sensor_data.sensor_type = self.extract_sensor_type(self.topic_url)
        sensor_data.sensor_group = self.extract_sensor_group(self.topic_url)

        # Initialize a dictionary to hold the payload data for logging
        data_dict = {}

        # Populate data_map based on the topic type
        if "ppg" in self.topic_url:
            sensor_data.data_map["led_1"] = struct.pack("i", random.randint(100, 110))
            data_dict["led_1"] = random.randint(100, 110)
            sensor_data.data_map["led_2"] = struct.pack("i", random.randint(100, 110))
            data_dict["led_2"] = random.randint(100, 110)
            sensor_data.data_map["led_3"] = struct.pack("i", random.randint(100, 110))
            data_dict["led_3"] = random.randint(100, 110)
            sensor_data.data_map["temperature"] = struct.pack("f", round(random.uniform(36.5, 37.5), 1))
            data_dict["temperature"] = round(random.uniform(36.5, 37.5), 1)

        elif "imu" in self.topic_url:
            sensor_data.data_map["acc_x"] = struct.pack("f", round(random.uniform(-0.03, 0.03), 2))
            data_dict["acc_x"] = round(random.uniform(-0.03, 0.03), 2)
            sensor_data.data_map["acc_y"] = struct.pack("f", round(random.uniform(-0.03, 0.03), 2))
            data_dict["acc_y"] = round(random.uniform(-0.03, 0.03), 2)
            sensor_data.data_map["acc_z"] = struct.pack("f", round(random.uniform(-0.03, 0.03), 2))
            data_dict["acc_z"] = round(random.uniform(-0.03, 0.03), 2)
            sensor_data.data_map["gyro_x"] = struct.pack("f", round(random.uniform(-0.2, 0.2), 2))
            data_dict["gyro_x"] = round(random.uniform(-0.2, 0.2), 2)
            sensor_data.data_map["gyro_y"] = struct.pack("f", round(random.uniform(-0.2, 0.2), 2))
            data_dict["gyro_y"] = round(random.uniform(-0.2, 0.2), 2)
            sensor_data.data_map["gyro_z"] = struct.pack("f", round(random.uniform(-0.2, 0.2), 2))
            data_dict["gyro_z"] = round(random.uniform(-0.2, 0.2), 2)
            sensor_data.data_map["mag_x"] = struct.pack("f", round(random.uniform(-0.05, 0.05), 2))
            data_dict["mag_x"] = round(random.uniform(-0.05, 0.05), 2)
            sensor_data.data_map["mag_y"] = struct.pack("f", round(random.uniform(-0.05, 0.05), 2))
            data_dict["mag_y"] = round(random.uniform(-0.05, 0.05), 2)
            sensor_data.data_map["mag_z"] = struct.pack("f", round(random.uniform(-0.05, 0.05), 2))
            data_dict["mag_z"] = round(random.uniform(-0.05, 0.05), 2)

        # Save data_dict for logging in the on_publish method
        self.payload_readable = data_dict

        # Serialize the Protobuf message
        return sensor_data.SerializeToString()


    def extract_pacifier_id(self, topic_url):
        return topic_url.split('/')[1]

    def extract_sensor_type(self, topic_url):
        return topic_url.split('/')[-1]

    def extract_sensor_group(self, topic_url):
        return "default_group"
