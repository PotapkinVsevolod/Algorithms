import pytest

from hashmap.hash_maps import HashMap

TEST_KEYS_FOR_OVERFLOW = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q']

def test_constants():
    assert HashMap.MAX_LOAD_FACTOR == 0.75
    assert HashMap.INITIAL_ALLOCATED_SIZE == 16
    assert HashMap.EXTENSION_DEGREE == 2

def test_init_len():
    assert len(HashMap()) == 0

def test_init_value():
    assert HashMap() == [None for _ in range(HashMap.INITIAL_ALLOCATED_SIZE)]

def test_add_one_key_value():
    hash_map = HashMap()
    hash_map['foo'] = 'bar'
    assert len(hash_map) == 1
    assert hash_map['foo'] == 'bar'

def test_change_value():
    hash_map = HashMap()
    hash_map['foo'] = 'bar'
    hash_map['foo'] = 'baz'
    assert len(hash_map) == 1
    assert hash_map['foo'] == 'baz'


def test_add_two_keys_with_same_hash():
    hash_map = HashMap()
    assert hash_map._get_hash('quuz') == hash_map._get_hash('corge')
    hash_map['quuz'] = 'foo'
    hash_map['corge'] = 'bar'
    assert len(hash_map) == 2
    assert hash_map['quuz'] == 'foo'
    assert hash_map['corge'] == 'bar'

def test_get_nonpresent_key():
    hash_map = HashMap()
    with pytest.raises(KeyError):
        hash_map['foo']

def test_hash_function_return_the_same_hash():
    hash_map = HashMap()
    assert hash_map._get_hash("foo") == hash_map._get_hash("foo")


def test_list_for_exist_of_12_unique_hashes():
    hash_map = HashMap()
    keys = TEST_KEYS_FOR_OVERFLOW
    hashes = set()
    for key in keys:
        hashes.add(hash_map._get_hash(key))
    assert len(hashes) == HashMap.INITIAL_ALLOCATED_SIZE * HashMap.MAX_LOAD_FACTOR

def test_overflow():
    hash_map = HashMap()
    count = 0
    for key in TEST_KEYS_FOR_OVERFLOW:
        hash_map[key] = count
        count += 1
    assert hash_map.allocated_slots == hash_map.INITIAL_ALLOCATED_SIZE * hash_map.EXTENSION_DEGREE
    assert len(hash_map) == len(TEST_KEYS_FOR_OVERFLOW)

def test_integer_key():
    hash_map = HashMap()
    hash_map[1] = 2
    assert hash_map[1] == 2

def test_none_key():
    hash_map = HashMap()
    hash_map[None] = 2
    assert hash_map[None] == 2