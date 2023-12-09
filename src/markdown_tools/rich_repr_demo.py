import rich.repr
import rich.console
from rich import print as rprint
from dataclasses import dataclass, field


class Bird0:
    def __init__(self, name, eats=None, fly=True, extinct=False):
        self.name = name
        self.eats = list(eats) if eats else []
        self.fly = fly
        self.extinct = extinct

    def __rich_repr__(self) -> rich.repr.Result:
        yield self.name
        yield "eats", self.eats
        yield "fly", self.fly, True
        yield "extinct", self.extinct, False


@rich.repr.auto
class Bird1:
    def __init__(self, name, eats=None, fly=True, extinct=False):
        self.name = name
        self.eats = list(eats) if eats else []
        self.fly = fly
        self.extinct = extinct


@dataclass
@rich.repr.auto
class Bird2:
    name: str
    eats: list[str] = field(default_factory=list)
    fly: bool = True
    extinct: bool = False


BIRDS0 = {
    "gull": Bird0(
        "gull", eats=["fish", "chips", "ice cream", "sausage rolls"]
    ),
    "penguin": Bird0("penguin", eats=["fish"], fly=False),
    "dodo": Bird0("dodo", eats=["fruit"], fly=False, extinct=True),
}

BIRDS1 = {
    "gull": Bird1(
        "gull", eats=["fish", "chips", "ice cream", "sausage rolls"]
    ),
    "penguin": Bird1("penguin", eats=["fish"], fly=False),
    "dodo": Bird1("dodo", eats=["fruit"], fly=False, extinct=True),
}


BIRDS2 = {
    "gull": Bird2(
        "gull", eats=["fish", "chips", "ice cream", "sausage rolls"]
    ),
    "penguin": Bird2("penguin", eats=["fish"], fly=False),
    "dodo": Bird2("dodo", eats=["fruit"], fly=False, extinct=True),
}


rprint(BIRDS0)
rprint(BIRDS1)
rprint(BIRDS2)
