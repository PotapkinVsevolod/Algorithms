import hashlib

class HashMap:

    MAX_LOAD_FACTOR = 2 / 3
    INITIAL_ALLOCATED_SIZE = 16
    EXTENSION_DEGREE = 2

    def __init__(self):
        self.allocated_size = __class__.INITIAL_ALLOCATED_SIZE
        self.size = 0
        self.storage = [None for _ in range(self.allocated_size)]

    def __eq__(self, value):
        return self.storage == value

    def __getitem__(self, key):
        key_hash = self._hash(key)
        try:
            key_index = self.storage[key_hash].index(key)
            return self.storage[key_hash][key_index + 1]
        except (ValueError, AttributeError):
            raise(KeyError)

    def __len__(self):
        return self.size

    def __setitem__(self, key, value):
        key_hash = self._hash(key)
        if self.storage[key_hash] == None:
            self.storage[key_hash] = [key, value]
            self.size += 1
            return
        try:
            key_index = self.storage[key_hash].index(key)
            self.storage[key_hash][key_index + 1] = value
        except ValueError:
            self.storage[key_hash] += [key, value]
            self.size += 1

    def _hash(self, key):
        return int(hashlib.sha256(key.encode('utf-8')).hexdigest(), 16) % self.allocated_size
