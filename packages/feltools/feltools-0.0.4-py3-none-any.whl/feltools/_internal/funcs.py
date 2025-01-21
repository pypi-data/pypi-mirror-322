def find_pos_in_arr(arr: list, value: int) -> int:
    for index, i in enumerate(arr):
        if value < i:
            return index
    return len(arr)