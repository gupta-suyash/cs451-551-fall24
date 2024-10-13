from collections import OrderedDict

class OD:
    def __init__(self):
        self.tree = OrderedDict()

    def insert(self, key, value):
        self.tree[key] = value

    def get(self, key):
        return self.tree.get(key)

    def minimum(self):
        return list(self.tree.values())[0]

    def maximum(self):
        return list(self.tree.vlaues())[-1]

    def contains_key(self, key):
        return self.tree.get(key) is not None