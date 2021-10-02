import typing as tp
from abc import ABCMeta, abstractmethod

from .event import Event


class EventHandler(metaclass=ABCMeta):
    def __init__(self):
        self._simulator_schedule_event_callback: tp.Optional[tp.Callable[[Event], None]] = None
        self._start_time: tp.Optional[float] = None

    @abstractmethod
    def handle_start(self) -> None:
        pass

    @abstractmethod
    def handle_stop(self) -> None:
        pass

    @abstractmethod
    def handle_event(self, event: Event) -> None:
        pass

    def set_simulator_schedule_event_callback(self,
                                              simulator_schedule_event_callback: tp.Callable[[Event], None]) -> None:
        self._simulator_schedule_event_callback = simulator_schedule_event_callback

    def set_start_time(self, start_time: float) -> None:
        self._start_time = start_time


