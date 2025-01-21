# This file is placed in the Public Domain.


"errors"


from ..runtime import Errors


def err(event):
    """ raised errors. """
    nmr = 0
    for exc in Errors.errors:
        for line in exc:
            event.reply(line.strip())
        nmr += 1
    if not nmr:
        event.reply("no errors")
        return
    event.reply(f"found {nmr} errors.")
