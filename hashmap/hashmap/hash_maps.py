import hashlib
from types import NoneType
from itertools import chain


class HashMap:

    MAX_LOAD_FACTOR = 0.75
    INITIAL_ALLOCATED_SIZE = 16
    EXTENSION_DEGREE = 2

    def __init__(self):
        self.allocated_slots = __class__.INITIAL_ALLOCATED_SIZE
        self.filled_slots = 0
        self.storage = [None for _ in range(self.allocated_slots)]

    def __getitem__(self, key):
        keyhash = self._get_hash(key)
        for index in chain(range(keyhash, self.allocated_slots), range(keyhash)):
            if not self.storage[index]:
                raise KeyError
            elif self.storage[index][0] == key:
                return self.storage[index][1]

    def __setitem__(self, key, value, new_storage=None):
        storage = new_storage if new_storage else self.storage
        keyhash = self._get_hash(key)
        for index in chain(range(keyhash, self.allocated_slots), range(keyhash)):
            if not storage[index] or storage[index][0] == key:
                self.filled_slots += 1 if not storage[index] else 0
                storage[index] = (key, value)
                break
        if self.filled_slots == self.allocated_slots * __class__.MAX_LOAD_FACTOR:
            self._restructure_storage()

    def _get_hash(self, key):
        if isinstance(key, int):
            byte_string = bin(key).encode("UTF-8")
        elif isinstance(key, NoneType):
            byte_string = bin(256).encode("UTF-8")
        elif isinstance(key, str):
            byte_string = key.encode("UTF-8")
        else:
            raise KeyError("Unhashable type of key.")
        return (
            int(
                hashlib.sha256(byte_string).hexdigest(),
                16,
            )
            % self.allocated_slots
        )

    def _restructure_storage(self):
        self.allocated_slots *= __class__.EXTENSION_DEGREE
        self.filled_slots = 0
        new_storage = [None for _ in range(self.allocated_slots)]
        for slot in self.storage:
            if slot:
                self.__setitem__(slot[0], slot[1], new_storage=new_storage)
        self.storage = new_storage

    def __eq__(self, value):
        return self.storage == value

    def __len__(self):
        return self.filled_slots
