# This file is placed in the Public Domain.


"fleet"


from rssbot.clients import Fleet
from rssbot.runtime import name


def flt(event):
    "list of bots."
    bots = Fleet.bots.values()
    try:
        event.reply(Fleet.bots[int(event.args[0])])
    except (IndexError, ValueError):
        event.reply(",".join([name(x).split(".")[-1] for x in bots]))
