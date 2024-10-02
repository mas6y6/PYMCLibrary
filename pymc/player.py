from .location import Location
from .exception import JavaException

class Player:
    def __init__(self,_raw_data: str, _conn):
        self._raw = _raw_data
        self._raw_split = _raw_data.split("*")
        self._raw_split.pop(0)
        self._conn = _conn
        self.username = self._raw_split[0]
        self.displayname = self._raw_split[1]
        self.uuid = self._raw_split[2]
    
    def getlocation(self) -> Location:
        self._conn._wb.send(f"!player*{self.uuid}*getloc")
        data = self._conn._recv()
        if data[0] == "~":
            raise JavaException(f"An error occurred {data.split('*')[1]}")
        return Location(data,self._conn)
    
    def giveitem(self,itemname: str,amount: int) -> None:
        self._conn._wb.send(f"!player*{self.uuid}*giveitem*{itemname}*{amount}")
        data = self._conn._recv()
        if data[0] == "~":
            raise JavaException(f"An error occurred {data.split('*')[1]}")