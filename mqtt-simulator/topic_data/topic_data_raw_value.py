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
