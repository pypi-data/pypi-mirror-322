from suid_core import system_pb2
from suid_core import system_pb2_grpc
from suid_core.core import serve, logging

from codetiming import Timer
from google.protobuf.json_format import (
    MessageToDict,
)

from machine import GCODEMachine as SimpleMachine, SerialEncoder as SeriaInterface, State
from machine import TCPMachine as SimpleTCPMachine, TCPEncoder, State

logger = logging.getLogger("MachineService")
class MachineServicer(system_pb2_grpc.MachineServicer):
    def __init__(self, device):
        super().__init__()
        if device.startswith('/dev/tty'):
            self.machine = SimpleMachine(
                SeriaInterface(
                    250000,
                    device,
                )
            )
            return
        device = device.split(':')
        self.machine = (
            SimpleTCPMachine(
                TCPEncoder(
                    device[0],
                    int(device[1]),
                    unit_id=1,
                    auto_open=True,
                    auto_close=False,
                    timeout=5
                )
            )
        )
        
    
    @Timer("configureState",  text="{name} elapsed time: {:.4f}s", logger=logger.debug)
    def configureState(self, request, context):
        request_info = MessageToDict(
            request,
            preserving_proto_field_name=True,
            use_integers_for_enums=False,
            including_default_value_fields=True,
        )
        self.machine.states = [State(state) for state in request_info['states']]
        return system_pb2.configureStateResult(states=request.states)
    
    @Timer("updateState",  text="{name} elapsed time: {:.4f}s", logger=logger.debug)
    def updateState(self, request, context):
        if len(request.info.objects)>0:
            _object = request.info.objects.pop(0)

            self.machine._object = _object

            for state in self.machine.states:
                print(
                    self.machine.send("G0 X{x} Y{y} Z{z} F5000".format(**state.value))
                )
        return system_pb2.updateStateResult(info=request.info)
    
    

if __name__ == '__main__':
    import argparse
    from threading import Event
    stop_signal = Event()

    parser = argparse.ArgumentParser(description="Client script for capturing images and sending commands to the model server.")
    parser.add_argument('--service_port', type=str, required=False, help="(PORT) where the this service are.", default="50051")
    parser.add_argument('--device', type=str, required=False, help="(DEVICE) Serial port/device address", default="/dev/ttyACM0")
    args = parser.parse_args()

    servicer = MachineServicer(args.device)
    serve(system_pb2_grpc.add_MachineServicer_to_server, servicer, logger, stop_signal, server_port=args.service_port)