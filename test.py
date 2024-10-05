import pymc, logging

import pymc.chat

link = pymc.PYMCLink("127.0.0.1")
while True:
    players = link.getallonlineplayers()
    for i in players:
        i.sendmessage(pymc.chat.ChatColor.AQUA+"he")