import pymc
from pymc.world import Weather
w = pymc.PYMCLink("localhost")
w.getworld("world").setweather(Weather.RAIN)