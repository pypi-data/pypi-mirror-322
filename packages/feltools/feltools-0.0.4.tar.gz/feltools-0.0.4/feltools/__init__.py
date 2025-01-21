import hashlib
from ._internal.funcs import find_pos_in_arr as find_index
from ._internal.err import ListEmptyError
def spec_hash(text: str) -> str:
    """
    Generate a combined SHA-256 and SHA-512 hash of the input text.
    
    Args:
        text (str): The input text to hash.
    
    Returns:
        str: The combined hash.
    """
    sha256 = hashlib.sha256()
    sha256.update(text.encode('utf-8'))
    sha256_digest = sha256.hexdigest()
    
    sha512 = hashlib.sha512()
    sha512.update(text.encode('utf-8'))
    sha512_digest = sha512.hexdigest()
    
    sha512_digest = sha512_digest[:len(sha256_digest)]
    return sha512_digest + sha256_digest

def insert_sort(arr: list, raise_error_on_list_empty=True) -> list:
    """
    Sort a list using the insertion sort algorithm.
    
    Args:
        arr (list): The list to sort.
        raise_err_on_list_empty (bool): Whether to raise an error if the list is empty. Defaults to True.
        
    Returns:
        list: The sorted list.
    """
    if not arr:
        if raise_error_on_list_empty:
            raise ListEmptyError(arr)
        return []
    
    sorted_arr = [arr[0]]
    for i in arr[1:]:
        index = find_index(sorted_arr, i)
        sorted_arr.insert(index, i)
    return sorted_arr
