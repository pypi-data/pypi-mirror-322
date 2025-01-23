from interface import State as StateInterface, Machine as MachineInterface, Encoder as EncoderInterface
from serial import Serial
import functools as ft

from pyModbusTCP.utils import (decode_ieee, encode_ieee, long_list_to_word,
                               word_list_to_long)

from pyModbusTCP.client import ModbusClient as TCPEncoder

class Object:
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def get(self, k, v):
        return getattr(self, str(k), v)

def get(x,y):
    if isinstance(x, dict):
        return x.get(y,y)
    return getattr(x,y,y)

class State(StateInterface):

    def __init__(self, _template, _object = {}):
        self._template = _template
        self._object = _object
    
    def get_value(self, _object = {}):
        obj = _object or self._object
        return {k: ft.reduce(get, [obj, *str(v).split('.')]) for k, v in self._template.items()} 

class SerialEncoder(EncoderInterface):
    def __init__(self, baudrate, port):
        self.baudrate = baudrate or 250000
        self.port = port
        if self.port is not None:
            self.serial = Serial(self.port, self.baudrate, timeout=2, write_timeout=2)
            while self.read() != ['']:
                self.read()

    def write(self, payload):
        self.serial.write((f"{payload}\n").encode("ascii"))
        self.last_value_send = payload
        return self.read()

    def read(self):
        lines = []
        _b = self.serial.readline()
        while _b != b"" and self.serial.inWaiting() != 0:
            lines.append(_b.decode("ascii").rstrip())
            _b = self.serial.readline()
        lines.append(_b.decode("ascii").rstrip())
        self.last_value_received = lines
        return lines    


class GCODEMachine(MachineInterface):
    def __init__(self, encoder:EncoderInterface, states: StateInterface=[]):
        self.encoder = encoder
        #self.__object = {'_pointer':50, 'y':50}
        self.states = states or [
            State({'x':'coordinate.x', 'y':'coordinate.y', 'z':5}),
            State({'x':0, 'y':0, 'z':263})
        ]
        self.homing()

    @property
    def _object(self):
        return self.__object
    
    @_object.setter
    def _object(self, value):
        for state in self.states:
            state._object = value

    def homing(self):
        self.send('G28')

    def send(self, message):
        self.encoder.write(message)
        self.encoder.write("M400")
        # self.encoder.write("M300 S440 P100")
        x = self.encoder.write("M118 finish")
        while "finish" not in x:
            x = self.encoder.read()
            print(x)
        self.encoder.write("M300 S440 P50")

class TCPMachine(MachineInterface):
    def __init__(self, encoder, address=[21000, 21004], states=[]):
        self.encoder = encoder
        self.address = address
        self.encoder.open()
        if not self.encoder.is_open:
            raise ConnectionRefusedError("Cant communicate with clp")

        self.states = states or [
            State({'x':'coordinate.x', 'y':'coordinate.y', 'z':5}),
        ]
    
    @property
    def _object(self):
        return self.__object
    
    @_object.setter
    def _object(self, value):
        for state in self.states:
            state._object = value

    def write_float(self, address, floats_list):
        """Write float(s) with write multiple registers."""
        b32_l = [int(f) for f in floats_list]
        print(b32_l)
        b16_l = long_list_to_word(b32_l)
        print(b16_l)
        return self.encoder.write_multiple_registers(address, b32_l)
    
    def read_float(self, address, number=1):
        """Read float(s) with read holding registers."""
        reg_l = self.encoder.read_holding_registers(address, number * 2)
        if reg_l:
            return reg_l# [decode_ieee(f) for f in word_list_to_long(reg_l)]
        else:
            return None
    
    def send(self, message):
        try:
            m = message.split(' ')
            match m[0]:
                case 'G0':
                    p = [int(float(m[i][1:])) for i in range(1, len(m))]
                    # print(p)
                    for a, v in zip(self.address, p):
                        self.write_float(a, [v])
        except ValueError as e:
            print(message, e)

    def homing():
        ...

if __name__ == '__main__':

    obj = Object(**{'x':50, 'y':50})
    obj2 = Object()
    obj2.coordinate = obj

    A = State({'x':50, 'y':50, 'z':263})
    B = State({'x':'x', 'y':'y', 'z':10},obj)
    C = State({'x':0, 'y':0, 'z':'z'}, {'z':263})

    encoder = SerialEncoder(250000, '/dev/ttyACM2')
    machine = GCODEMachine(encoder)

    machine._object = obj2
    for state in machine.states:
        machine.send("G0 X{x} Y{y} Z{z} F15000".format(**state.value))

    machine._object = {'coordinate':{'x':-50, 'y':-50}}#obj

    for state in machine.states:
        machine.send("G0 X{x} Y{y} Z{z} F15000".format(**state.value))

    

    # print(A.get_value(), B.get_value(obj), C.get_value())
