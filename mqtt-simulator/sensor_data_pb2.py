# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: sensor_data.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'sensor_data.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11sensor_data.proto\x12\x06Protos\"\xaf\x01\n\nSensorData\x12\x13\n\x0bpacifier_id\x18\x01 \x01(\t\x12\x13\n\x0bsensor_type\x18\x02 \x01(\t\x12\x14\n\x0csensor_group\x18\x03 \x01(\t\x12\x31\n\x08\x64\x61ta_map\x18\x04 \x03(\x0b\x32\x1f.Protos.SensorData.DataMapEntry\x1a.\n\x0c\x44\x61taMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x02\x38\x01\"\x94\x02\n\x07IMUData\x12#\n\x05gyros\x18\x01 \x03(\x0b\x32\x14.Protos.IMUData.gyro\x12!\n\x04mags\x18\x02 \x03(\x0b\x32\x13.Protos.IMUData.mag\x12!\n\x04\x61\x63\x63s\x18\x03 \x03(\x0b\x32\x13.Protos.IMUData.acc\x1a\x36\n\x04gyro\x12\x0e\n\x06gyro_x\x18\x01 \x01(\x02\x12\x0e\n\x06gyro_y\x18\x02 \x01(\x02\x12\x0e\n\x06gyro_z\x18\x03 \x01(\x02\x1a\x32\n\x03mag\x12\r\n\x05mag_x\x18\x01 \x01(\x02\x12\r\n\x05mag_y\x18\x02 \x01(\x02\x12\r\n\x05mag_z\x18\x03 \x01(\x02\x1a\x32\n\x03\x61\x63\x63\x12\r\n\x05\x61\x63\x63_x\x18\x01 \x01(\x02\x12\r\n\x05\x61\x63\x63_y\x18\x02 \x01(\x02\x12\r\n\x05\x61\x63\x63_z\x18\x03 \x01(\x02\"\xb9\x01\n\x07PPGData\x12!\n\x04leds\x18\x01 \x03(\x0b\x32\x13.Protos.PPGData.led\x12\x31\n\x0ctemperatures\x18\x02 \x03(\x0b\x32\x1b.Protos.PPGData.temperature\x1a\x32\n\x03led\x12\r\n\x05led_1\x18\x01 \x01(\x05\x12\r\n\x05led_2\x18\x02 \x01(\x05\x12\r\n\x05led_3\x18\x03 \x01(\x05\x1a$\n\x0btemperature\x12\x15\n\rtemperature_1\x18\x01 \x01(\x02\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sensor_data_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SENSORDATA_DATAMAPENTRY']._loaded_options = None
  _globals['_SENSORDATA_DATAMAPENTRY']._serialized_options = b'8\001'
  _globals['_SENSORDATA']._serialized_start=30
  _globals['_SENSORDATA']._serialized_end=205
  _globals['_SENSORDATA_DATAMAPENTRY']._serialized_start=159
  _globals['_SENSORDATA_DATAMAPENTRY']._serialized_end=205
  _globals['_IMUDATA']._serialized_start=208
  _globals['_IMUDATA']._serialized_end=484
  _globals['_IMUDATA_GYRO']._serialized_start=326
  _globals['_IMUDATA_GYRO']._serialized_end=380
  _globals['_IMUDATA_MAG']._serialized_start=382
  _globals['_IMUDATA_MAG']._serialized_end=432
  _globals['_IMUDATA_ACC']._serialized_start=434
  _globals['_IMUDATA_ACC']._serialized_end=484
  _globals['_PPGDATA']._serialized_start=487
  _globals['_PPGDATA']._serialized_end=672
  _globals['_PPGDATA_LED']._serialized_start=584
  _globals['_PPGDATA_LED']._serialized_end=634
  _globals['_PPGDATA_TEMPERATURE']._serialized_start=636
  _globals['_PPGDATA_TEMPERATURE']._serialized_end=672
# @@protoc_insertion_point(module_scope)
