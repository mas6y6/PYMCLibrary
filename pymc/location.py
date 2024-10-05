from .world import World
from .block import Block

class Location:
    def __init__(self,_raw,_conn):
        self._raw = _raw
        self._conn = _conn
        self._raw_split = _raw["return"].split("*")
        self.dimension = self._raw_split[0]
        self.worldname = self._raw_split[1]
        self.x = self._raw_split[2]
        self.y = self._raw_split[3]
        self.z = self._raw_split[4]
        self.direction = self._raw_split[5]
        self.pitch = self._raw_split[6]
        self.yaw = self._raw_split[7]
    
    def getworld(self):
        id = self._conn._send("!world*{self.worldname}*getworld")
        return World(self._conn._recv(id),self._conn)
    
    def getblock(self):
        id = self._conn._send(f"!location*{self.dimension}*{self.worldname}*{self.x}*{self.y}*{self.z}*{self.pitch}*{self.direction}*{self.yaw}*getblock")
        return Block(self._conn._recv(id),self._conn)