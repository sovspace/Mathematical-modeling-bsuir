
import typing as tp

from collections import deque

T = tp.TypeVar('T')


class Queue(tp.Generic[T]):
    def __init__(self):
        self._elements_queue: tp.Deque[T] = deque()
        self._removed_set: tp.Set[T] = set()

    def push(self, element: T) -> None:
        self._elements_queue.append(element)

    def pop(self) -> T:
        popped_element = self._elements_queue.pop()
        while popped_element in self._removed_set:
            self._removed_set.remove(popped_element)
            popped_element = self._elements_queue.pop()
        return popped_element

    def remove(self, element: T):
        self._removed_set.add(element)

    def __contains__(self, item):
        return item not in self._removed_set and item in self._elements_queue

    def __len__(self):
        return len(self._elements_queue) - len(self._removed_set)
