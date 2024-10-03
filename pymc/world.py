from .block import Block

class Environment:
    OVERWORLD = "NORMAL"
    NETHER = "NETHER"
    END = "THE_END"
    CUSTOM = "CUSTOM"
    
class Weather:
    CLEAR = "CLEAR"
    THUNDER = "THUNDERSTORM"
    RAIN = "RAIN"

class World:
    def __init__(self,_raw,_conn):
        self._raw = _raw
        self._conn = _conn
        self._raw_split = _raw.split("*")
        self._raw_split.pop(0)
        self.world_name = self._raw_split[0]
        self.environment = None
        if self._raw_split[1] == "NORMAL":
            self.environment = Environment.OVERWORLD
        if self._raw_split[1] == "NORMAL":
            self.environment = Environment.NETHER
        if self._raw_split[1] == "NORMAL":
            self.environment = Environment.END
        else:
            self.environment = Environment.CUSTOM

        self.minheight = int(self._raw_split[2])
        self.maxheight = int(self._raw_split[3])
        self.seed = self._raw_split[4]
        self.difficulty = self._raw_split[5]
        self.logicalheight = self._raw_split[6]
        
    def setweather(self,weather: Weather):
        if weather == Weather.CLEAR:
            self._conn._wb.send(f"!world*{self.world_name}*setweather*false*false")
        elif weather == Weather.RAIN:
            self._conn._wb.send(f"!world*{self.world_name}*setweather*true*false")
        elif weather == Weather.THUNDER:
            self._conn._wb.send(f"!world*{self.world_name}*setweather*true*true")