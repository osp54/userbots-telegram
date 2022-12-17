from typing import Callable, Type

from pyrogram import filters
from pyrogram.handlers.handler import Handler


def command(name: str | list[str], desc: str = "Not provided description", prefixes: str | list[str] = "/"):
    def decorator(function: Callable):
        setattr(function, "command", {
            "name": name,
            "prefixes": prefixes,
            "function": function,
            "desc": desc
        })
        return function

    return decorator


def on_event(event: Type[Handler], event_filter: filters = filters.all):
    def decorator(function: Callable):
        setattr(function, "event", {
            "event": event,
            "filter": event_filter,
            "function": function
        })
        return function

    return decorator
