from abc import ABC, abstractmethod

class Encoder(ABC):
    
    @abstractmethod
    def write(payload):
        pass

    @abstractmethod
    def read():
        pass


class State(ABC):    
    
    @abstractmethod
    def get_value(self):
        pass

    @property
    def value(self):
        return self.get_value()


class Machine(ABC):
    def __init__(self, encoder:Encoder):
        self.encoder = encoder
    
    @abstractmethod
    def send(self, message):
        self.encoder.write(message)
        return self.encoder.read()
    
    @abstractmethod
    def homing():
        pass