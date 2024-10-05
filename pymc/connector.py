import websockets.sync.client, requests, traceback
from .player import Player
from .exception import JavaException, NullError, BukkitError
from .world import Environment, World
from .block import Block
from threading import Thread
import json, random, logging, time, threading, ast


class PYMCLink:
    def __init__(self, host: str, port=8290, ssl=None, logger=None, debug=False):
        self.logger = logger
        print(f"Connecting to PyMC at {host}:{port} ...")
        self._wb = websockets.sync.client.connect(f"ws://{host}:{port}", ssl=ssl)
        print("Successfully connected!")
        self._handshakedata = self._wb.recv()
        self._thread = Thread(target=self._threadrecv)
        self._recv_buffer = {}
        self._thread.start()
        self._lock = threading.Lock()
        print("Started buffer thread")
        self.debug = debug

    # Packet Codes
    # "!" Command (Send or Recv)
    # "%" Ping
    # "~~" Error Packet

    def _threadrecv(self):
        while True:
            try:
                rawdata = self._wb.recv()
                data = json.loads(rawdata)
                uid = data["id"]
                with self._lock:
                    self._recv_buffer[uid] = data
            except Exception as e:
                traceback.print_exc()


    def _send(self, data):
        uid = random.randint(000000, 999999)
        self._wb.send(f"!{uid}*"+data)
        return uid

    def _recv(self, uid):
        while True:
            if str(uid) in self._recv_buffer:
                data = self._recv_buffer[str(uid)]
                self._recv_buffer.pop(str(uid))
                return data
            time.sleep(0.1)  # Delay to avoid busy waiting

    def _format_uuid(self, raw_uuid):
        if len(raw_uuid) != 32:
            raise ValueError("Invalid UUID length. It should be 32 characters.")

        # Insert hyphens in the appropriate places to conform to UUID format
        formatted_uuid = (
            raw_uuid[:8]
            + "-"
            + raw_uuid[8:12]
            + "-"
            + raw_uuid[12:16]
            + "-"
            + raw_uuid[16:20]
            + "-"
            + raw_uuid[20:]
        )

        return formatted_uuid

    def getplayerbyusername(self, username: str):
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        try:
            response = requests.get(url)
        except:  # noqa: E722
            traceback.print_exc()

        if response.status_code == 200:
            data = response.json()
            uid = self._send(f"player*{self._format_uuid(data['id'])}*getplayer")
            data = self._recv(uid)
            if data["status"] == "error":
                raise JavaException(data["return"])

            if not data["return"] == "nonexist":
                return Player(data["return"], self)
            else:
                return None
        else:
            raise ConnectionError(
                f"Error: Unable to fetch data for player '{username}' (Status code: {response.status_code})"
            )

    def getplayerbyuuid(self, uuid):
        uid = self._send(f"player*{uuid}*getplayer")
        data = self._recv(uid)
        if data["status"] == "error":
            raise JavaException(data["return"])

        if not data["return"] == "nonexist":
            return Player(data["return"], self)
        else:
            return None

    def getworld(self, worldname: str):
        uid = self._send(f"world*{worldname}*getworld")
        data = self._recv(uid)
        if data["status"] == "error":
            raise JavaException(data["return"])
        else:
            return World(data["return"], self)

    def getallonlineplayers(self):
        uid = self._send("bukkit*getallonlineplayers")
        data = self._recv(uid)
        list = []
        if data["status"] == "error":
            raise JavaException(data["return"])
        else:
            e = ast.literal_eval(data["return"])
            for i in e:
                list.append(Player({"return":i}, self))
            return list
    
    def getallofflineplayers(self):
        uid = self._send("bukkit*getallofflineplayers")
        data = self._recv(uid)
        list = []
        if data["status"] == "error":
            raise JavaException(data["return"])
        else:
            e = ast.literal_eval(data["return"])
            for i in e:
                list.append(i)
            return list

    def close(self):
        self._wb.close()
