from .world import World

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
    
    def getWorld(self):
        self._conn._wb.send("!world")
        return World(self._conn._recv(),self._conn)