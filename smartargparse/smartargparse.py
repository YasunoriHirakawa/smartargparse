import dataclasses
from argparse import ArgumentParser
from typing import Type, TypeVar


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
        field.type = field.type
        is_required = (
            field.default is dataclasses.MISSING or field.default is None)
        if field.type is bool:
            if field.default is True:
                parser.add_argument(argument, action="store_false")
            else:
                parser.add_argument(argument, action="store_true")
            continue
        if is_required:
            parser.add_argument(
                argument, type=field.type, required=is_required,
                help=f"type: {field.type.__name__}, required")
        else:
            parser.add_argument(
                argument, type=field.type, default=field.default,
                help=f"type: {field.type.__name__}, default: {field.default}")

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
        int_w_default: int = 1
        float_w_default: float = 1.0
        str_w_default: str = "foo"
        bool_w_default: bool = True

    config = parse_args(Config)
    print(vars(config))


if __name__ == "__main__":
    test()
