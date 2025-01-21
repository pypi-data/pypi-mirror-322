from threading import Lock, Thread
from time import sleep
from typing import Any, Callable

from jthreads.looping_thread import LoopingThread


class Timer(Thread):
    """
    Timer is a class providing delayed execution for a given callback.
    It can be cancelled at any time before the time ellapses. The cancellation
    polling interval is 1 second.

    """

    __slots__ = ("__time", "__cancelPollingTime", "__callback", "__canceled", "__lock")

    def __init__(
        self, time: float, cancelPollingTime: float, callback: Callable[[], Any]
    ) -> None:
        """
        Constructor.

        Args:
            time (float): Number of seconds until execution
            cancelPollingTime (float): Number of seconds at which this timer will poll for cancel flag
            callback (Callable[[], Any]): The callback to be executed
        """
        if time <= 0 or cancelPollingTime <= 0:
            raise ValueError(
                "time and cancelPollingTime parameters must be higher than 0"
            )

        if cancelPollingTime >= time:
            raise ValueError("cancelPollingTime cannot be higher than time")

        self.__time = time
        self.__cancelPollingTime = cancelPollingTime
        self.__callback: Callable[[], Any] = callback
        self.__canceled: bool = False
        self.__lock = Lock()
        Thread.__init__(self)

    def cancel(self) -> None:
        """
        Cancel this timer.
        """
        with self.__lock:
            self.__canceled = True

    def run(self) -> None:
        while self.__time > 0:
            sleep(self.__cancelPollingTime)
            self.__time = self.__time - self.__cancelPollingTime
            with self.__lock:
                if self.__canceled:
                    return
        shouldExecute = False
        with self.__lock:
            if not self.__canceled:
                shouldExecute = True
        if shouldExecute:
            self.__callback()


class Interval(LoopingThread):
    """
    This thread calls the given callback at the given interval, until canceled.
    """

    __slots__ = ("__interval", "__callback")

    def __init__(self, interval: float, callback: Callable[[], Any]) -> None:
        """
        The interval thread calls the given callback at intervals defined by the interval parameter (in seconds).

        Args:
            interval (float): The interval at which the callback will be called
            callback (Callable[[], Any]): The callback

        Raises:
            ValueError: _description_
        """
        LoopingThread.__init__(self)
        if interval <= 0:
            raise ValueError("interval parameter must be higher than 0")
        self.__interval = interval
        self.__callback = callback

    def loop(self) -> None:
        sleep(self.__interval)
        self.__callback()


__all__ = ["Timer", "Interval"]
