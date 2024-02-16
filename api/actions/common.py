from typing import Any


def remove_none_values_from_dict(data: dict[Any:Any]):
    return dict(filter(lambda a: a[1] is not None, data.items()))
