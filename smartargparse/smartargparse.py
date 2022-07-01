import dataclasses
from argparse import ArgumentParser
from typing import Type, TypeVar


class BaseConfig:
    def __init__(self, *_):
        pass


T = TypeVar("T", bound=BaseConfig)


def parse_args(config: Type[T]) -> T:

    parser = ArgumentParser()

    for key, value in vars(config)["__dataclass_fields__"].items():
        argument = "--" + key.replace("_", "-")
        value_type = value.type
        is_required = (
            type(value.default) is dataclasses._MISSING_TYPE
            or value.default is None)
        if value_type is bool:
            if value.default is True:
                parser.add_argument(argument, action="store_false")
            else:
                parser.add_argument(argument, action="store_true")
            continue
        if is_required:
            parser.add_argument(
                argument, type=value_type, required=is_required,
                help=f"type: {value_type.__name__}, required")
        else:
            parser.add_argument(
                argument, type=value_type, default=value.default,
                help=f"type: {value_type.__name__}, default: {value.default}")

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
