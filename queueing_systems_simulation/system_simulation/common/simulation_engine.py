import typing as tp
import heapq

from .event import Event
from .event_handler import EventHandler


class SimulationEngine:
    START_CALLBACK: str = "start"
    STOP_CALLBACK: str = "stop"
    EVENT_CALLBACK: str = "event"

    def __init__(self, start_time: float, finish_time: float) -> None:
        self._event_list: tp.List[Event] = []

        self._start_time: float = start_time
        self._finish_time: float = finish_time

        self._callback_dict: tp.Dict[str, tp.List[tp.Callable]] = {self.START_CALLBACK: [], self.STOP_CALLBACK: [],
                                                                   self.EVENT_CALLBACK: []}

    def start(self) -> None:
        self._notify_start()
        while self._event_list:
            event = heapq.heappop(self._event_list)
            self._notify_event(event)
        self._notify_stop()

    def schedule(self, event: Event) -> None:
        if event.time < self._finish_time:
            heapq.heappush(self._event_list, event)

    def register_callback(self, func: tp.Callable, callback_type: str) -> None:
        self._callback_dict[callback_type].append(func)

    def register_event_handler(self, event_handler: EventHandler) -> None:
        self.register_callback(event_handler.handle_start, SimulationEngine.START_CALLBACK)
        self.register_callback(event_handler.handle_stop, SimulationEngine.STOP_CALLBACK)
        self.register_callback(event_handler.handle_event, SimulationEngine.EVENT_CALLBACK)

        event_handler.set_simulator_schedule_event_callback(self.schedule)
        event_handler.set_start_time(self._start_time)

    def _notify_start(self) -> None:
        for func in self._callback_dict[self.START_CALLBACK]:
            func()

    def _notify_stop(self) -> None:
        for func in self._callback_dict[self.STOP_CALLBACK]:
            func()

    def _notify_event(self, event: Event) -> None:
        for func in self._callback_dict[self.EVENT_CALLBACK]:
            func(event)
