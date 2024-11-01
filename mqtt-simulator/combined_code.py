# Collected Files:
# - main.py
# - simulator.py
# - topic.py
# - utils.py
# - broker_settings.py
# - client_settings.py
# - __init__.py
# - topic_data.py
# - topic_data_bool.py
# - topic_data_math_expression.py
# - topic_data_number.py
# - topic_data_raw_value.py
# - __init__.py
# Total files collected: 13

le = Path(arg)
    if not settings_file.is_file():
        return parser.error(f"argument -f/--file: can't open '{arg}'")
    return settings_file

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', dest='settings_file', type=lambda x: is_valid_file(parser, x), help='settings file', default=default_settings())
args = parser.parse_args()

simulator = Simulator(args.settings_file)
simulator.run()

# --- End of main.py ---


# --- Start of simulator.py ---
# simulator.py
import json
from topic import Topic
from data_classes import BrokerSettings, ClientSettings

class Simulator:
    def __init__(self, settings_file):
        self.default_client_settings = ClientSettings(
            clean=True,
            retain=False,
            qos=2,
            time_interval=10
        )
        self.topics = self.load_topics(settings_file)

    def read_client_settings(self, settings_dict: dict, default: ClientSettings):
        return ClientSettings(
            clean=settings_dict.get('CLEAN_SESSION', default.clean),
            retain=settings_dict.get('RETAIN', default.retain),
            qos=settings_dict.get('QOS', default.qos),
            time_interval=settings_dict.get('TIME_INTERVAL', default.time_interval)
        )

    def load_topics(self, settings_file):
        topics = []
        with open(settings_file) as json_file:
            config = json.load(json_file)
            broker_settings = BrokerSettings(
                url=config.get('BROKER_URL', 'localhost'),
                port=config.get('BROKER_PORT', 1883),
                protocol=config.get('PROTOCOL_VERSION', 4) # mqtt.MQTTv311
            )
            broker_client_settings = self.read_client_settings(config, default=self.default_client_settings)
            for topic in config['TOPICS']:
                topic_data = topic['DATA']
                topic_payload_root = topic.get('PAYLOAD_ROOT', {})
                topic_client_settings = self.read_client_settings(topic, default=broker_client_settings)
                if topic['TYPE'] == 'single':
                    topic_url = topic['PREFIX']
                    topics.append(Topic(broker_settings, topic_url, topic_data, topic_payload_root, topic_client_settings))
                elif topic['TYPE'] == 'multiple':
                    for id in range(topic['RANGE_START'], topic['RANGE_END']+1):
                        topic_url = topic['PREFIX'] + '/' + str(id)
                        topics.append(Topic(broker_settings, topic_url, topic_data, topic_payload_root, topic_client_settings))
                elif topic['TYPE'] == 'list':
                    for item in topic['LIST']:
                        topic_url = topic['PREFIX'] + '/' + str(item)
                        topics.append(Topic(broker_settings, topic_url, topic_data, topic_payload_root, topic_client_settings))
        return topics

    def run(self):
        while True:
            for topic in self.topics:
                print(f'Starting: {topic.topic_url} ...')
                topic.start()
            for topic in self.topics:
                topic.join()

# --- End of simulator.py ---


# --- Start of topic.py ---
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

        if "ppg" in self.topic_url:
            payload["heart_rate"] = random.randint(70, 80)
            payload["oxygen"] = random.randint(96, 99)
            payload["acc_x"] = round(random.uniform(-0.03, 0.03), 2)
            payload["acc_y"] = round(random.uniform(-0.03, 0.03), 2)
            payload["acc_z"] = round(random.uniform(-0.03, 0.03), 2)
        elif "imu" in self.topic_url:
            payload["gyro_x"] = round(random.uniform(-0.2, 0.2), 2)
            payload["gyro_y"] = round(random.uniform(-0.2, 0.2), 2)
            payload["gyro_z"] = round(random.uniform(-0.2, 0.2), 2)

        has_data_active = True
        return payload if has_data_active else None

# --- End of topic.py ---


# --- Start of utils.py ---
import random

def should_run_with_probability(probability: float):
    random_number = random.random()
    return random_number < probability

# --- End of utils.py ---


# --- Start of broker_settings.py ---
from dataclasses import dataclass

@dataclass
class BrokerSettings:
    url: str
    port: int
    protocol: int

# --- End of broker_settings.py ---


# --- Start of client_settings.py ---
from dataclasses import dataclass

@dataclass
class ClientSettings:
    clean: bool
    retain: bool
    qos: int
    time_interval: int

# --- End of client_settings.py ---


# --- Start of __init__.py ---
from .broker_settings import *
from .client_settings import *

# --- End of __init__.py ---


# --- Start of topic_data.py ---
from abc import ABC, abstractmethod
from utils import should_run_with_probability

class TopicData(ABC):
    def __init__(self, data):
        self.data = data
        self.name = data['NAME']
        self.is_active = True
        self.old_value = None

    def generate_value(self):
        new_value = None
        if self.old_value is None:
            # generate initial data
            if 'INITIAL_VALUE' in self.data:
                new_value = self.data['INITIAL_VALUE']
            else:
                new_value = self.generate_initial_value()
        else:
            # generate next data
            if should_run_with_probability(self.data.get('RETAIN_PROBABILITY', 0)):
                new_value = self.old_value
            elif should_run_with_probability(self.data.get('RESET_PROBABILITY', 0)):
                new_value = self.generate_initial_value()
            else:
                new_value = self.generate_next_value()
        self.old_value = new_value
        return new_value

    @abstractmethod
    def generate_initial_value(self):
        pass

    @abstractmethod
    def generate_next_value(self):
        pass

# --- End of topic_data.py ---


# --- Start of topic_data_bool.py ---
import random
from .topic_data import TopicData

class TopicDataBool(TopicData):
    def __init__(self, data):
        super().__init__(data)

    def generate_initial_value(self):
        return random.choice([True, False])

    def generate_next_value(self):
        return not self.old_value # can be kept the same according to RETAIN_PROBABILITY

# --- End of topic_data_bool.py ---


# --- Start of topic_data_math_expression.py ---
import math
import random
from .topic_data import TopicData

class TopicDataMathExpression(TopicData):
    def __init__(self, data):
        super().__init__(data)
        self.expression_evaluator = None

    def generate_initial_value(self):
        self.expression_evaluator = ExpressionEvaluator(self.data['MATH_EXPRESSION'], self.data['INTERVAL_START'], self.data['INTERVAL_END'], self.data['MIN_DELTA'], self.data['MAX_DELTA'])
        return self.expression_evaluator.get_current_expression_value()

    def generate_next_value(self):
        return self.expression_evaluator.get_next_expression_value()


class ExpressionEvaluator():
    def __init__(self, math_expression, interval_start, interval_end, min_delta, max_delta):
        self._math_expression = self.generate_compiled_expression(math_expression)
        self._interval_start = interval_start
        self._interval_end = interval_end
        self._min_delta = min_delta
        self._max_delta = max_delta
        self._x = interval_start

    def get_current_expression_value(self):
        return self._math_expression(self._x)

    def get_next_expression_value(self):
        if self._x > self._interval_end:
            self._x = self._interval_start
            return self.get_current_expression_value()
        step = random.uniform(self._min_delta, self._max_delta)
        self._x += step
        return self.get_current_expression_value()

    def generate_compiled_expression(self, expression):
        lambda_expression = "lambda x: "+expression
        code = compile(lambda_expression, "<string>", "eval")
        ALLOWED_FUNCTIONS = {function_name: func for function_name, func in math.__dict__.items() if not function_name.startswith("__")}
        for name in code.co_names:
            if name not in ALLOWED_FUNCTIONS:
                raise NameError(f"The use of '{name}' is not allowed")
        return eval(code, {"__builtins__": {}, "math":math}, ALLOWED_FUNCTIONS)

# --- End of topic_data_math_expression.py ---


# --- Start of topic_data_number.py ---
import random
from .topic_data import TopicData
from utils import should_run_with_probability

class TopicDataNumber(TopicData):
    def __init__(self, data):
        super().__init__(data)
        self.is_int = data['TYPE'] == 'int'

    def generate_initial_value(self):
        if self.is_int:
            # int number
            return random.randint(self.data['MIN_VALUE'], self.data['MAX_VALUE'])
        else:
            # float number
            return random.uniform(self.data['MIN_VALUE'], self.data['MAX_VALUE'])

    def generate_next_value(self):
        if self.data.get('RESTART_ON_BOUNDARIES', False) and (self.old_value == self.data.get('MIN_VALUE') or self.old_value == self.data.get('MAX_VALUE')):
            return self.generate_initial_value()
        step = random.uniform(0, self.data['MAX_STEP'])
        step = round(step) if self.is_int else step
        increase_probability = self.data['INCREASE_PROBABILITY'] if 'INCREASE_PROBABILITY' in self.data else 0.5
        if should_run_with_probability(1 - increase_probability):
            step *= -1
        return max(self.old_value + step, self.data['MIN_VALUE']) if step < 0 else min(self.old_value + step, self.data['MAX_VALUE'])

# --- End of topic_data_number.py ---


# --- Start of topic_data_raw_value.py ---
# topic_data_raw_value.py
from .topic_data import TopicData

class TopicDataRawValue(TopicData):
    def __init__(self, data):
        super().__init__(data)
        self.raw_values_index = 0

    def generate_initial_value(self):
        self.raw_values_index = self.data.get('INDEX_START', 0)
        return self.get_current_value()

    def generate_next_value(self):
        end_index = self.data.get('INDEX_END', len(self.data['VALUES']) - 1)
        self.raw_values_index += 1
        if self.raw_values_index <= end_index:
            return self.get_current_value()
        elif self.raw_values_index > end_index and self.data.get('RESTART_ON_END', False):
            self.raw_values_index = self.data.get('INDEX_START', 0)
            return self.generate_initial_value()
        else:
            self.is_active = False

    def get_current_value(self):
        current_value_for_index = self.data['VALUES'][self.raw_values_index]
        if 'VALUE_DEFAULT' in self.data:
            value = {}
            value.update(self.data.get('VALUE_DEFAULT', {}))
            value.update(current_value_for_index)
            return value
        return current_value_for_index

# --- End of topic_data_raw_value.py ---


# --- Start of __init__.py ---
from .topic_data_number import TopicDataNumber
from .topic_data_bool import TopicDataBool
from .topic_data_raw_value import TopicDataRawValue
from .topic_data_math_expression import TopicDataMathExpression

# --- End of __init__.py ---

