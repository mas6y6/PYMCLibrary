from .location import Location
from .exception import JavaException, BukkitError

class Player:
    def __init__(self,_raw_data: str, _conn):
        self._raw = _raw_data
        self._raw_split = _raw_data.split("*")
        self._raw_split.pop(0)
        self._conn = _conn
        self.username = self._raw_split[0]
        self.displayname = self._raw_split[1]
        self.customname = self._raw_split[2]
        self.uuid = self._raw_split[3]
        if self._raw_split[4] == Gamemode.SURVIVAL:
            self.gamemode = Gamemode.SURVIVAL
        elif self._raw_split[4] == Gamemode.CREATIVE:
            self.gamemode = Gamemode.CREATIVE
        elif self._raw_split[4] == Gamemode.ADVENTURE:
            self.gamemode = Gamemode.ADVENTURE
        elif self._raw_split[4] == Gamemode.SPECTATOR:
            self.gamemode = Gamemode.SPECTATOR
        self.health = self._raw_split[5]
        self.healthscale = self._raw_split[6]
        self.xp = self._raw_split[7]
        self.xptolevel = self._raw_split[8]
        self.xplevel = self._raw_split[9]
        self.exhaustion = self._raw_split[10]
        self.foodlevel = self._raw_split[11]
        self.saturation = self._raw_split[12]
        self.starvationrate = self._raw_split[13]
        self.freezeticks = self._raw_split[14]
        self.remainingair = self._raw_split[15]
        self.playertime = self._raw_split[16]
        self.freezeticks = self._raw_split[14]
        self.remainingair = self._raw_split[15]
        self.playertime = self._raw_split[16]
        self.lastplayed = self._raw_split[17]
        self.sleepticks = self._raw_split[18]
        self.flyspeed = self._raw_split[20]
        self.fireticks = self._raw_split[21]
        self.address = self._raw_split[22]
        self.latency = self._raw_split[23]
        
    def getlocation(self) -> Location:
        self._conn._wb.send(f"!player*{self.uuid}*getloc")
        data = self._conn._recv()
        if data[0] == "~":
            raise JavaException(f"An error occurred {data.split('*')[1]}")
        return Location(data,self)
    
    def giveitem(self,itemname: str,amount: int) -> None:
        self._conn._wb.send(f"!player*{self.uuid}*giveitem*{itemname}*{amount}")
        data = self._conn._recv()
        if data[0] == "~":
            raise JavaException(f"An error occurred {data.split('*')[1]}")
    
    def removeitem(self,itemname: str,amount: int) -> None:
        self._conn._wb.send(f"!player*{self.uuid}*removeitem*{itemname}*{amount}")
        data = self._conn._recv()
        if data[0] == "~":
            raise JavaException(f"An error occurred {data.split('*')[1]}")
    
    def sendmessage(self,message: str) -> None:
        self._conn._wb.send(f"!player*{self.uuid}*sendmessage*{message}")
        data = self._conn._recv()
        if data[0] == "~":
            raise JavaException(f"An error occurred {data.split('*')[1]}")
    
    def sendtitle(self,title: str,subtitle: str,fadein=10,stay=70,fadeout=20) -> None:
        self._conn._wb.send(f"!player*{self.uuid}*sendtitle*{title}*{subtitle}*{fadein}*{stay}*{fadeout}")
        data = self._conn._recv()
        if data[0] == "~":
            raise JavaException(f"An error occurred {data.split('*')[1]}")
    
    def sendactionbar(self,message: str) -> None:
        self._conn._wb.send(f"!player*{self.uuid}*sendactionbar*{message}")
        data = self._conn._recv()
        if data[0] == "~":
            raise JavaException(f"An error occurred {data.split('*')[1]}")
    
    def addeffect(self,potion: str, duration: int, amplifier: int) -> None:
        self._conn._wb.send(f"!player*{self.uuid}*addeffect*{potion}*{duration}*{amplifier}")
        data = self._conn._recv()
        if data[0] == "~":
            raise JavaException(f"An error occurred {data.split('*')[1]}")
        elif data.split("*")[1] == "potionnotfound":
            raise BukkitError("Potion Not Found")
    
    def removeeffect(self,potion: str) -> None:
        self._conn._wb.send(f"!player*{self.uuid}*removeeffect*{potion}")
        data = self._conn._recv()
        if data[0] == "~":
            raise JavaException(f"An error occurred {data.split('*')[1]}")
        elif data.split("*")[1] == "potionnotfound":
            raise BukkitError("Potion Not Found")
        

class Difficulty:
    PEACEFUL = "PEACEFUL"
    EASY = "EASY"
    NORMAL = "NORMAL"
    HARD = "HARD"

class Gamemode:
    SURVIVAL = "SURVIVAL"
    CREATIVE = "CREATIVE"
    ADVENTURE = "ADVENTURE"
    SPECTATOR = "SPECTATOR"