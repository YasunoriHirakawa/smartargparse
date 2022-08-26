import dataclasses
import typing
from argparse import ArgumentParser
from typing import List, Type, TypeVar


class BaseConfig:
    def __init__(self, *_):
        pass


T = TypeVar("T", bound=BaseConfig)


def parse_args(config: Type[T]) -> T:

    if not dataclasses.is_dataclass(config):
        raise TypeError("Argument must be dataclass")

    parser = ArgumentParser()

    for field in dataclasses.fields(config):
        argument = "--" + field.name.replace("_", "-")
        nargs = "*" if typing.get_origin(field.type) is list else None
        argtype = field.type if nargs is None else typing.get_args(field.type)[0]
        is_required = (
            (field.default is dataclasses.MISSING or field.default is None) and
            (field.default_factory is dataclasses.MISSING or field.default_factory is None))
        if nargs == "*" and field.default_factory is not dataclasses.MISSING:
            raise ValueError("Default value is not supported for lists")

        if field.type is bool:
            if field.default is True:
                parser.add_argument(argument, action="store_false")
            else:
                parser.add_argument(argument, action="store_true")
            continue
        if is_required:
            parser.add_argument(
                argument, type=argtype, required=is_required, nargs=nargs,  # type: ignore
                help=f"type: {argtype.__name__}, required")
        else:
            parser.add_argument(
                argument, type=argtype, default=field.default, nargs=nargs,  # type: ignore
                help=f"type: {argtype.__name__}, default: {field.default}")

    args = vars(parser.parse_args())
    args = {key: value for key, value in args.items() if value is not None}
    return config(**args)


def test() -> None:

    @dataclasses.dataclass(frozen=True)
    class Config(BaseConfig):
        int_wo_default: int
        float_wo_default: float
        str_wo_default: str
        bool_wo_default: bool
        list_wo_default: List[int]
        int_w_default: int = 1
        float_w_default: float = 1.0
        str_w_default: str = "foo"
        bool_w_default: bool = True

    config = parse_args(Config)
    print(vars(config))


if __name__ == "__main__":
    test()
