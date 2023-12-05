from typing import TypeAlias


class Command:
    pass


class Event:
    pass


Message: TypeAlias = Command | Event
