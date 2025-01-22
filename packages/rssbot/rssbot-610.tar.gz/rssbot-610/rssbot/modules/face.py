# This file is placed in the Public Domain.
# ruff: noqa: F401


"interface"


from rssbot.modules import cmd, err, flt, irc, mod, opm, rss, thr, upt


def __dir__():
    return (
        'cmd',
        'err',
        'flt',
        'irc',
        'mod',
        'opm',
        'rss',
        'thr',
        'upt'
    )


__all__ = __dir__()
