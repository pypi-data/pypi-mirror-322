import threading


class SingletonMeta(type):
    _instance = None
    _lock: threading.Lock = threading.Lock()  # Ensures thread-safe singleton

    def __call__(cls, *args, **kwargs):  # type: ignore
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance
