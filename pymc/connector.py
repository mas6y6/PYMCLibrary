import websockets.sync.client

class PYMCLink:
    def __init__(self,host: str,port=8290):
        self.wb = websockets.sync.client.connect(f"ws://{host}:{port}")
        self._handshakedata = self.wb.recv()