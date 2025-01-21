from threading import Thread
from time import sleep
from typing import Any, Callable


class CountdownTimer(Thread):
    """
    CountdownTimer is similar to Timer, but doesn't poll for cancellation.
    This is a fire and forget timer that unconditionally executes the callback
    once the time has ellapsed.
    """

    __slots__ = ("__timeout", "__callback")

    def __init__(self, timeout: float, callback: Callable[[], Any]) -> None:
        """
        Constructor. This object cannot be cancelled. Once started, the callback will be
        unconditionally executed after the given time has ellapsed. This implementation
        is an optimization of the Timer class in the sense that it doesn't periodically
        poll for a cancel state.

        Args:
            timeout (float): The number of seconds that should pass until the execution of the callback
            callback (Callable[[], Any]): The callback function
        """
        Thread.__init__(self)
        if timeout <= 0:
            raise ValueError("timeout parameter must be higher than 0")

        self.__timeout = timeout
        self.__callback = callback

    def run(self) -> None:
        sleep(self.__timeout)
        self.__callback()


__all__ = ["CountdownTimer"]
