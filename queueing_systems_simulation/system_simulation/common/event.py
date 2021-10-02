import typing as tp


class Event:
    def __init__(self, identifier: str, time: float, customer_id: tp.Optional[int] = None,
                 **kwargs: tp.Dict[str, tp.Any]) -> None:
        self._identifier = identifier
        self._time = time
        self._customer_id = customer_id
        self._data = kwargs

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def time(self) -> float:
        return self._time

    @property
    def customer_id(self) -> tp.Optional[int]:
        return self._customer_id

    @property
    def data(self) -> tp.Dict[str, tp.Any]:
        return self._data

    def __lt__(self, other: 'Event') -> bool:
        return self._time < other._time
