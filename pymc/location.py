from .world import World
from .block import Block

class Location:
    def __init__(self,_raw,_conn):
        self._raw = _raw
        self._conn = _conn
        self._raw_split = _raw.split("*")
        self.dimension = self._raw_split[1]
        self.worldname = self._raw_split[2]
        self.x = self._raw_split[3]
        self.y = self._raw_split[4]
        self.z = self._raw_split[5]
        self.direction = self._raw_split[6]
        self.pitch = self._raw_split[7]
        self.yaw = self._raw_split[8]
    
    def getworld(self):
        self._conn._wb.send(f"!world*{self.worldname}*getworld")
        return World(self._conn._recv(),self._conn)
    
    def getblock(self):
        self._conn._wb.send(f"!location*{self.dimension}*{self.worldname}*{self.x}*{self.y}*{self.z}*{self.pitch}*{self.direction}*{self.yaw}*getblock")
        return Block(self._conn._recv(),self._conn)