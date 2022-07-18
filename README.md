# smartargparse
Convenience wrapper of python for configuring ArgumentParser using a class.

## Install
```sh
pip3 install https://github.com/YasunoriHirakawa/smartargparse/archive/main.zip
```

## Usage
### First import this module.  
```python
from smartargparse import BaseConfig, parse_args
```

### Then Prepare dataclass.  
```python
@dataclasses.dataclass(frozen=True)
class Car(BaseConfig):
    name: str
    displacement: float
    max_speed: int = 180
    is_used: bool = False
```
The field type can be int, float, str, or bool.  

Fields of type bool are treated as flags.  
If the initial value is False or no initial value is given, a flag is generated that becomes True when called as an argument.  
If the initial value is True, the opposite is the case.

For non-bool types, if an initial value is set, it is used as the default value for the argument.  
Fields with no initial value will be required arguments.

### To construct an ArgumentParser from this class, write the following:
```python
car = parse_args(Car)
```

---

In the end, the above code is equivalent to the following code.
```python
from argparse import ArgumentParser

@dataclasses.dataclass(frozen=True)
class Car:
    name: str
    displacement: float
    max_speed: int
    is_used: bool

pasrser = ArgumentParser()
parser.add_argument("name", type=str, required=True, help="type: str, required")
parser.add_argument("displacement", type=float, required=True, help="type: float, required")
parser.add_argument("max_speed", type=int, default=180, help="type: int, default: 180")
parser.add_argument("is_used", action="store_true")
args = parser.parse_args()

car = Car(
    args["name"],
    args["displacement"],
    args["max_speed"],
    args["is_used"])
```
