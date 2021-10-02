import typing as tp

import pandas as pd
import numpy as np

from ..common.event_handler import EventHandler
from ..common.event import Event


class MultichannelWithWarmingUpEventHandler(EventHandler):
    ARRIVAL_EVENT = 'arrival_event'
    SERVICE_EVENT = 'service_event'

    def __init__(self, channels_count: int, arrival_rate: float, service_rate: float,
                 warming_up_rate: float, filename_to_save_logs: str) -> None:
        super().__init__()
        self._channels_count = channels_count
        self._arrival_rate = arrival_rate
        self._service_rate = service_rate
        self._warming_up_rate = warming_up_rate
        self._filename_to_save_logs = filename_to_save_logs

        self._last_arrived_customer_id = 0
        self._busy_channels_count = 0
        self._customers_log: tp.Dict[int, tp.Dict[str, float]] = {}

    def handle_start(self) -> None:
        if self._simulator_schedule_event_callback is None or self._start_time is None:
            raise Exception

        self._simulator_schedule_event_callback(
            Event(self.ARRIVAL_EVENT, self._start_time, self._last_arrived_customer_id))

    def handle_stop(self) -> None:
        df = pd.DataFrame(data=self._customers_log.values(), index=self._customers_log.keys())
        df.to_csv(self._filename_to_save_logs)  # noqa

    def handle_event(self, event: Event):
        if event.identifier is self.ARRIVAL_EVENT:
            self._customers_log[event.customer_id] = {f'{self.ARRIVAL_EVENT}_time': event.time}
            self._busy_channels_count += 1
            self._schedule_service_event(event.time, event.customer_id)
            if self._busy_channels_count < self._channels_count:
                self._schedule_arrival_event(event.time)

        elif event.identifier is self.SERVICE_EVENT:
            self._customers_log[event.customer_id][f'{self.SERVICE_EVENT}_time'] = event.time
            if self._busy_channels_count == self._channels_count:
                self._schedule_arrival_event(event.time)
            self._busy_channels_count -= 1

    def _schedule_arrival_event(self, base_time: float) -> None:
        arrival_delta_time = np.random.exponential(1.0 / self._arrival_rate)
        self._last_arrived_customer_id += 1
        arrival_event = Event(self.ARRIVAL_EVENT, base_time + arrival_delta_time, self._last_arrived_customer_id)
        self._simulator_schedule_event_callback(arrival_event)

    def _schedule_service_event(self, base_time: float, customer_id: int) -> None:
        warming_up_delta_time = np.random.exponential(1.0 / self._warming_up_rate)
        service_delta_time = np.random.exponential(1.0 / self._service_rate)
        service_event = Event(self.SERVICE_EVENT, base_time + service_delta_time + warming_up_delta_time, customer_id)
        self._simulator_schedule_event_callback(service_event)
