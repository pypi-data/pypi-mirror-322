from threading import Thread
from typing import Any, Callable

__all__ = ['CountdownTimer']

class CountdownTimer(Thread):
    def __init__(self, timeout: float, callback: Callable[[], Any]) -> None: ...
    def run(self) -> None: ...
