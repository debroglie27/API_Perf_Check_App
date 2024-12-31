from gevent._semaphore import Semaphore


class DebugSemaphore(Semaphore):
    def __init__(self, value=1):
        super().__init__(value)
        self._debug_value = value

    def acquire(self, *args, **kwargs):
        result = super().acquire(*args, **kwargs)
        if result:
            self._debug_value -= 1
            print(f"Semaphore acquired. Current value: {self._debug_value}")
        return result

    def release(self):
        super().release()
        self._debug_value += 1
        print(f"Semaphore released. Current value: {self._debug_value}")

    @property
    def value(self):
        return self._debug_value


# Shared semaphore instance
all_users_complete = DebugSemaphore(0)
