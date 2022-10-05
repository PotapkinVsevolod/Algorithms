from datetime import datetime, timedelta

import pytest

from hashmap.hash_maps import HashMap

TEST_KEYS_FOR_OVERFLOW = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
]


class TestUsingOfDifferentTypesAsKey:
    def test_integer(self):
        hash_map = HashMap()
        hash_map[1] = 2
        assert hash_map[1] == 2

    def test_none(self):
        hash_map = HashMap()
        hash_map[None] = 2
        assert hash_map[None] == 2

    def test_set(self):
        hash_map = HashMap()
        with pytest.raises(KeyError):
            hash_map[{1, 2}] = 2

    def test_dict(self):
        hash_map = HashMap()
        with pytest.raises(KeyError):
            hash_map[{"a": 1}] = 2

    def test_list(self):
        hash_map = HashMap()
        with pytest.raises(KeyError):
            hash_map[[]] = 2


class TestInitializationParameters:
    def test_add_init_allocated_size(self):
        hash_map = HashMap(1001)
        assert hash_map.allocated_slots == 1001

    def test_add_str_as_init_allocated_size(self):
        with pytest.raises(TypeError):
            hashmap = HashMap("asda")

    def test_constants(self):
        assert HashMap.MAX_LOAD_FACTOR == 0.75
        assert HashMap.EXTENSION_DEGREE == 2

    def test_init_len(self):
        assert len(HashMap()) == 0

    def test_init_value(self):
        hashmap = HashMap()
        assert hashmap == [None for _ in range(hashmap.allocated_slots)]


def test_add_one_key_value():
    hash_map = HashMap()
    hash_map["foo"] = "bar"
    assert len(hash_map) == 1
    assert hash_map["foo"] == "bar"


def test_change_value():
    hash_map = HashMap()
    hash_map["foo"] = "bar"
    hash_map["foo"] = "baz"
    assert len(hash_map) == 1
    assert hash_map["foo"] == "baz"


def test_add_two_keys_with_same_hash():
    hash_map = HashMap()
    assert hash_map._get_hash("quuz") == hash_map._get_hash("corge")
    hash_map["quuz"] = "foo"
    hash_map["corge"] = "bar"
    assert len(hash_map) == 2
    assert hash_map["quuz"] == "foo"
    assert hash_map["corge"] == "bar"


def test_get_nonpresent_key():
    hash_map = HashMap()
    with pytest.raises(KeyError):
        hash_map["foo"]


def test_hash_function_return_the_same_hash():
    hash_map = HashMap()
    assert hash_map._get_hash("foo") == hash_map._get_hash("foo")


def test_overflow():
    hash_map = HashMap()
    allocated_slots = hash_map.allocated_slots
    for key in TEST_KEYS_FOR_OVERFLOW:
        hash_map[key] = "foo"
    assert hash_map.allocated_slots == allocated_slots * hash_map.EXTENSION_DEGREE
    assert len(hash_map) == len(TEST_KEYS_FOR_OVERFLOW)


def test_item_is_tuple():
    hash_map = HashMap()
    hash_map["foo"] = "bar"
    item = hash_map.storage[hash_map._get_hash("foo")]
    assert isinstance(item, tuple)

def test_performance():
    hashmap = HashMap(150000)
    
    assert hashmap.filled_slots == 0
    time_before = datetime.now()
    hashmap[0] = [0]
    first_set_time = (datetime.now() - time_before).microseconds

    for _ in range(1, 9):
        hashmap[_] = _
    
    assert hashmap.filled_slots == 9
    time_before = datetime.now()
    hashmap[10] = [10]
    tenth_set_time = (datetime.now() - time_before).microseconds

    for _ in range(11, 100):
        hashmap[_] = _

    assert hashmap.filled_slots == 99
    time_before = datetime.now()
    hashmap[100] = [100]
    hundredth_set_time = (datetime.now() - time_before).microseconds

    for _ in range(101, 1000):
        hashmap[_] = _

    assert hashmap.filled_slots == 999
    time_before = datetime.now()
    hashmap[1000] = [1000]
    thousandth_set_time = (datetime.now() - time_before).microseconds

    for _ in range(1001, 10000):
        hashmap[_] = _

    assert hashmap.filled_slots == 9999
    time_before = datetime.now()
    hashmap[10000] = [10000]
    ten_thousandth_set_time = (datetime.now() - time_before).microseconds

    for _ in range(10001, 100000):
        hashmap[_] = _

    assert hashmap.filled_slots == 99999
    time_before = datetime.now()
    hashmap[100000] = [100000]
    hundred_thousandth_set_time = (datetime.now() - time_before).microseconds

    print(f'1 - {first_set_time} microseconds')
    print(f'10 - {tenth_set_time} microseconds')
    print(f'100 - {hundredth_set_time} microseconds')
    print(f'1000 - {thousandth_set_time} microseconds')
    print(f'10000 - {ten_thousandth_set_time} microseconds')
    print(f'100000 - {hundred_thousandth_set_time} microseconds')

    assert False