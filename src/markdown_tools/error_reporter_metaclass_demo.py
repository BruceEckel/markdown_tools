from typing import Any, Callable
from pprint import pprint


class ErrorReporter:
    def __init__(self):
        self.logs = []

    def log(self, message: str):
        self.logs.append(message)


# Global instance
error_reporter = ErrorReporter()


class LoggingMeta(type):
    def __new__(
        cls, name: str, bases: tuple[type, ...], dct: dict[str, Any]
    ):
        # Wrap each method with a logging wrapper
        for attr_name, attr_value in dct.items():
            if callable(attr_value):
                dct[attr_name] = cls.log_method(attr_name, attr_value)
        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def log_method(method_name: str, method: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            # Log the method call
            arg_str = ", ".join(map(str, args)) + ", ".join(
                f"{k}={v}" for k, v in kwargs.items()
            )
            error_reporter.log(
                f"Calling {method_name} with arguments: {arg_str}"
            )

            # Call the original method
            return method(*args, **kwargs)

        return wrapper


class MyClass(metaclass=LoggingMeta):
    def method_a(self, n: int):
        # Method implementation...
        pass

    def method_b(self, s: str):
        # Method implementation...
        pass


obj = MyClass()
obj.method_a(5)
obj.method_b("test")

pprint(error_reporter.logs)
