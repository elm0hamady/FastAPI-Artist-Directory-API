from typing import Annotated,get_args,get_origin,get_type_hints
from functools import wraps


def my_decorator(func):
    @wraps(func)
    def wrapper(x):

        type_hints = get_type_hints(func,include_extras=True)
        hint = type_hints['x']
        if get_origin(hint) is Annotated:
            _,*hint_args = get_args(hint)
            low , high = hint_args[0]

            if not low <= x <= high :
                raise ValueError(f"{x} should be betwwen {low} and {high}")
            
        return func(x)
    return wrapper

@my_decorator
def double(x:Annotated[int,(0,100)])-> int:
    return x*2


re = double(131)
print(re)