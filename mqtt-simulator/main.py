import argparse
import os
from pathlib import Path
from grpc_tools import protoc
from simulator import Simulator

def default_settings():
    base_folder = Path(__file__).resolve().parent.parent
    settings_file = base_folder / 'config/settings.json'
    return settings_file

def is_valid_file(parser, arg):
    settings_file = Path(arg)
    if not settings_file.is_file():
        return parser.error(f"argument -f/--file: can't open '{arg}'")
    return settings_file


def compile_proto():
    proto_file = "sensor_data.proto"
    output_file = "sensor_data_pb2.py"

    if not os.path.exists(output_file) or os.path.getmtime(proto_file) > os.path.getmtime(output_file):
        print("Compiling Protobuf file using grpcio-tools...")
        result = protoc.main((
            '',
            f'--python_out=.',
            proto_file,
        ))
        if result != 0:
            print("Error compiling Protobuf file.")
            exit(1)
        else:
            print("Protobuf file compiled successfully.")

# Compile the Protobuf file if needed
compile_proto()

# Parse settings file argument
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', dest='settings_file', type=lambda x: is_valid_file(parser, x), help='settings file', default=default_settings())
args = parser.parse_args()

# Initialize and run the simulator
simulator = Simulator(args.settings_file)
simulator.run()
