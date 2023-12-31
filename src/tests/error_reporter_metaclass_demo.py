from typing import Any, Callable
from functools import wraps
import sys
from rich import print
from dataclasses import dataclass


class ErrorReporter:
    def __init__(self):
        self.trace = []

    def assert_true(self, condition: bool, msg: str) -> None:
        if not condition:
            self.error(msg)

    def error(self, msg: str) -> None:
        print(
            f"[bold red underline][ERROR][/bold red underline]\n{self}\n"
            f"[bold red]{msg}[/bold red]\n"
        )
        sys.exit(1)

    def track(self, message: str):
        self.trace.append(message)

    def __str__(self) -> str:
        return "\n".join(self.trace)


check = ErrorReporter()


# Decorator for standalone functions
def call_track(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        arg_str = ", ".join(map(str, args)) + ", ".join(
            f"{k}={v}" for k, v in kwargs.items()
        )
        check.track(f"{func.__name__}({arg_str})")
        # Call the original function
        return func(*args, **kwargs)

    return wrapper


# Metaclass to track method calls in classes
class CallTracker(type):
    def __new__(
        cls, name: str, bases: tuple[type, ...], dct: dict[str, Any]
    ):
        # Wrap each method with a logging wrapper
        for attr_name, attr_value in dct.items():
            if callable(attr_value):
                dct[attr_name] = cls.track_method(
                    attr_name, attr_value
                )
        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def track_method(method_name: str, method: Callable) -> Callable:
        def wrapper(self, *args, **kwargs):
            arg_str = ", ".join(map(str, args)) + ", ".join(
                f"{k}={v}" for k, v in kwargs.items()
            )
            check.track(
                f"{self.__class__.__name__}.{method_name}({arg_str})"
            )
            # Call the original method
            return method(self, *args, **kwargs)

        return wrapper


if __name__ == "__main__":

    @call_track
    def some_function(a, b):
        # Function implementation
        pass

    class MyClass(metaclass=CallTracker):
        def method_a(self, n: int):
            # Method implementation...
            pass

        def method_b(self, s: str):
            # Method implementation...
            pass

    @dataclass
    class Foo(metaclass=CallTracker):
        bob: str
        n: int

        def f(self, nn: int) -> None:
            self.n = nn

    some_function(1, 2)
    obj = MyClass()
    obj.method_a(5)
    obj.method_b("test")
    foo = Foo("hi", 20)
    foo.f(11)
    print(foo)

    check.assert_true(False, "Test error message")
