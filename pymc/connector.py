import websockets.sync.client, requests, traceback
from .player import Player
from .exception import JavaException, NullError, BukkitError
from .world import Environment, World
from .block import Block

class PYMCLink:
    def __init__(self,host: str, port=8290, ssl=None):
        self._wb = websockets.sync.client.connect(f"ws://{host}:{port}",ssl=ssl)
        self._handshakedata = self._wb.recv()
        self._pingdata = None
    
    # Packet Codes
    # "!" Command (Send or Recv)
    # "%" Ping
    # "~~" Error Packet
    
    def _recv(self):
        data = self._wb.recv()
        if data[0].lower() == "!".lower():
            return data[0:]
    
    def _format_uuid(self,raw_uuid):
        if len(raw_uuid) != 32:
            raise ValueError("Invalid UUID length. It should be 32 characters.")
        
        # Insert hyphens in the appropriate places to conform to UUID format
        formatted_uuid = (raw_uuid[:8] + '-' +
                        raw_uuid[8:12] + '-' +
                        raw_uuid[12:16] + '-' +
                        raw_uuid[16:20] + '-' +
                        raw_uuid[20:])
        
        return formatted_uuid
        
    def getplayerbyusername(self,username:str):
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        try:
            response = requests.get(url)
        except:
            traceback.print_exc()
            raise ConnectionError("An error occurred while connecting to Mojang API servers")

        if response.status_code == 200:
            data = response.json()
            self._wb.send(f"!player*{self._format_uuid(data['id'])}*getplayer")
            data = self._recv()
            if data[0] == "~":
                raise JavaException(data[0:])
            if not data == "!nonexist":
                return Player(data,self)
            else:
                raise BukkitError("Player not found")
        else:
            raise ConnectionError(f"Error: Unable to fetch data for player '{username}' (Status code: {response.status_code})")
    
    def getplayerbyuuid(self,uuid):
        self._wb.send(f"!player*{uuid}*getplayer")
        data = self._recv()
        if data[0] == "~":
            raise JavaException(data[0:])
        if not data == "!nonexist":
            return Player(data,self)
        else:
            raise BukkitError("Player not found")
    
    def getworld(self,string: str):
        self._wb.send(f"!world*{string}*getworld")
        data = self._recv()
        if data[0] == "~":
            raise JavaException(data[0:])
        else:
            return World(data[0:],self)
    
    def close(self):
        self._wb.close()