import pymc
from pymc.world import Weather

link = pymc.PYMCLink("127.0.0.1")
while True:
    print(link.getplayerbyusername("mas6y6").health)