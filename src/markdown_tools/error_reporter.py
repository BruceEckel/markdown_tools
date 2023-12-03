from pathlib import Path
from typing import Any, Callable, List, NoReturn
from functools import wraps
import sys
from .console import console
from dataclasses import dataclass


class ErrorReporter:
    def __init__(self) -> None:
        self.trace: List[str] = []
        self.input_file: Path | None = None
        self.current_line_number: int = 0
        self.current_line: str = ""

    def track(self, message: str) -> None:
        self.trace.append(message)

    def __str__(self) -> str:
        parts = []

        if self.input_file:
            parts.append(f"Input file: {self.input_file}")

        if self.current_line_number != 0:
            parts.append(f"At line number {self.current_line_number}")

        if self.current_line:
            parts.append(f"Line: {self.current_line}")

        parts.extend(self.trace)
        return "\n".join(parts)

    def __rich__(self) -> str:
        return str(self)

    def format(self, msg: str) -> str:
        return (
            f"[bold red underline][ERROR][/bold red underline]\n{self}\n"
            f"[bold red]{msg}[/bold red]\n"
        )

    def error(self, msg: str) -> NoReturn:
        console.print(self.format(msg))
        sys.exit(1)

    def is_true(self, condition: bool, msg: str) -> None:
        if not condition:
            self.error(msg)


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
    console.print(foo)

    # calls error():
    check.is_true(False, "Test error message")
