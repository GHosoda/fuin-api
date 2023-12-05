from typing import Awaitable, Callable, Deque, Self, TypeAlias

from app._typing import Command, Event, Message

CommandHandlers: TypeAlias = dict[
    type[Command], Callable[[Command], Awaitable[None | list[Event]]]
]
EventHandlers: TypeAlias = dict[type[Event], Callable[[Event], Awaitable[None]]]


class MessageBus:
    __instances: dict[str, Self] = {}
    command_handlers: CommandHandlers
    event_handlers: EventHandlers

    def __new__(
        cls,
        name: str = "__main__",
        command_handlers: None | CommandHandlers = None,
        event_handlers: None | EventHandlers = None,
    ) -> Self:
        if name not in cls.__instances:
            cls.__instances[name] = super().__new__(cls)
            cls.__instances[name].command_handlers = command_handlers or {}
            cls.__instances[name].event_handlers = event_handlers or {}
        return cls.__instances[name]

    async def __handle_command(self, command: Command) -> list[Event]:
        print(type(self.command_handlers))
        command_events = await self.command_handlers[type(command)](command)
        return command_events or []

    async def __handle_event(self, event: Event) -> None:
        ...

    async def handle(self, message: Message) -> None:
        messages = Deque([message])
        while messages:
            _message = messages.popleft()
            if isinstance(_message, Command):
                messages.extend(await self.__handle_command(_message))
            elif isinstance(message, Event):
                await self.__handle_event(message)
            else:
                raise TypeError(
                    f"Message must be either a `Command` or `Event`. Received `{type(_message)}`."
                )
