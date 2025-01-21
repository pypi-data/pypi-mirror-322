class ListEmptyError(Exception):
    def __init__(self, arr):
        self.msg = f"List is empty: {arr}"
    def __str__(self):
        return self.msg