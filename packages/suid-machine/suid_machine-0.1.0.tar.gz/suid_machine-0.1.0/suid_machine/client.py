import grpc
from suid_core import system_pb2_grpc
from suid_core import system_pb2

"""
            {
                'axis':{
                    'x':10,
                    'y':10,
                    'z':100
                },
                'actuators':[False, False],
            },
            {
                'axis':{
                    'x':0,
                    'y':0,
                    'z':200
                },
                'actuators':[True, True],
            },
"""

def update_state(stub: system_pb2_grpc.MachineStub, states=None):
    return stub.updateState(states)

def set_state(stub: system_pb2_grpc.MachineStub, states=None):
    return stub.configureState(states)

def run(host, port):
    conf_request = system_pb2.configureStateRequest(
        states= [{
                'x':'coordinate.x',
                'y':'coordinate.y',
                'z':'200'
            }],
        actuators=[False]
    )

    request = system_pb2.updateStateRequest(
        info={'objects':[
            {
                'coordinate':{
                    'x':10,
                    'y':10,
                    'z':100
                }
            },
        ]}
    )

    with grpc.insecure_channel(f"{host}:{port}") as channel:
        stub = system_pb2_grpc.MachineStub(channel)
        resp = stub.configureState(conf_request)
        request = stub.updateState(request)
        print(resp)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Client script for capturing images and sending commands to the model server.")
    parser.add_argument('-P','--service_port', type=str, required=False, help="(PORT) where the this service are.", default="50051")
    parser.add_argument('-H','--service_host', type=str, required=False, help="(HOST) where the this service are.", default="localhost")
    args = parser.parse_args()

    run(args.service_host, args.service_port)