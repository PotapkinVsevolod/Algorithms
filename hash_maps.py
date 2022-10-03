from calendar import c
import hashlib

class HashMap:

    MAX_LOAD_FACTOR = 0.75
    INITIAL_ALLOCATED_SIZE = 16
    EXTENSION_DEGREE = 2

    def __init__(self):
        self.allocated_slots = __class__.INITIAL_ALLOCATED_SIZE
        self.filled_slots = 0
        self.storage = [None for _ in range(self.allocated_slots)]
        self.number_of_items_in_storage = 0

    def __getitem__(self, key):
        keyhash = self._get_hash(key)
        if self.storage[keyhash] == None:
            raise KeyError
        for item in self.storage[keyhash]:
            if item[0] == key:
                return item[1]
        else:
            raise KeyError

    def __setitem__(self, key, value, new_storage=None):
        storage = self.storage if new_storage == None else new_storage
        keyhash = self._get_hash(key)
        if storage[keyhash] == None:
            storage[keyhash] = [[key, value]]
            if not new_storage:
                self.number_of_items_in_storage += 1
                self.filled_slots += 1
                if self.filled_slots == self.allocated_slots * __class__.MAX_LOAD_FACTOR:
                    self._restructure_storage()
            return
        for item in storage[keyhash]:
            if item[0] == key:
                item[1] = value
                break
        else:
            storage[keyhash].append([key, value])
            if not new_storage:
                self.number_of_items_in_storage += 1

    def _get_hash(self, key):
        return int(hashlib.sha256(str(key).encode('utf-8')).hexdigest(), 16) % self.allocated_slots
    
    def _restructure_storage(self):
        self.allocated_slots *= __class__.EXTENSION_DEGREE
        new_storage = [None for _ in range(self.allocated_slots)]
        self.filled_slots = 0
        for slot in self.storage:
            if slot == None:
                continue
            for item in slot:
                self.__setitem__(item[0], item[1], new_storage=new_storage)
        self.storage = new_storage

    def __eq__(self, value):
        return self.storage == value

    def __len__(self):
        return self.number_of_items_in_storage

    def __str__(self):
        return str(self.storage)
