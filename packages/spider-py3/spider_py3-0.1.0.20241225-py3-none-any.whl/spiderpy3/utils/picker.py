import random
from typing import List, Callable, Any


def get_random_pick(data: List[Any]) -> Callable[[], Any]:
    """

    :param data:
    :return:
    """
    shuffled_data = data[:]
    random.shuffle(shuffled_data)
    current_index = 0

    def random_pick() -> Any:
        nonlocal shuffled_data, current_index
        if current_index >= len(shuffled_data):
            shuffled_data = data[:]
            random.shuffle(shuffled_data)
            current_index = 0
        selected_item = shuffled_data[current_index]
        current_index += 1
        return selected_item

    return random_pick
