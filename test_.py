import pytest
from hash_maps import HashMap

def test_constants():
    assert HashMap.MAX_LOAD_FACTOR == 2 / 3
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
    assert hash_map._hash("foo") == hash_map._hash("foo")


def test_extension():
    hash_map = HashMap()
    keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    hashes = set()
    count = 0
    for key in keys:
        hashes.add(hash_map._hash(key))
        hash_map[key] = count
        count += 1
    assert len(hashes) > HashMap.INITIAL_ALLOCATED_SIZE * HashMap.MAX_LOAD_FACTOR
    