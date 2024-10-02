import pymc
w = pymc.PYMCLink("127.0.0.1")
print(w.getplayerbyuuid("df741692-5394-4da3-8079-bd25ba797dae")._raw)
