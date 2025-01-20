# test_fame_session_cache.py

import pytest

from famegui_runtime_helper.fame_session_cache import FameSessionCache


# Helper function to create unique items
def create_item(index):
    return {"item": f"Item {index}"}


@pytest.fixture(autouse=True)
def reset_cache():
    """
    Fixture to reset the FameSessionCache singleton before each test.
    """
    cache = FameSessionCache()
    cache.items.clear()
    cache.redo_items.clear()
    yield
    cache.items.clear()
    cache.redo_items.clear()


def test_singleton_behavior():
    """
    Test that FameSessionCache follows the singleton pattern.
    """
    cache1 = FameSessionCache()
    cache2 = FameSessionCache()
    assert cache1 is cache2, "FameSessionCache instances are not the same (singleton failed)."


def test_add_item():
    """
    Test adding unique items to the cache.
    """
    cache = FameSessionCache()
    item = create_item(1)
    cache.add_item(item)

    assert len(cache.get_items()) == 1
    assert cache.get_items()[0] == item


def test_add_duplicate_item():
    """
    Test that adding a duplicate item does not increase the cache size.
    """
    cache = FameSessionCache()
    item = create_item(1)
    cache.add_item(item)
    cache.add_item(item)  # Attempt to add duplicate

    assert len(cache.get_items()) == 1, "Duplicate item was added to the cache."


def test_max_size_limit():
    """
    Test that the cache does not exceed the maximum number of undo steps.
    """
    cache = FameSessionCache()
    max_steps = cache.MAX_UNDO_STEPS

    for i in range(max_steps + 2):  # Add more items than max
        cache.add_item(create_item(i))

    assert len(cache.get_items()) == max_steps, f"Cache exceeded max size of {max_steps}."
    expected_items = [create_item(i) for i in range(2, max_steps + 2)]
    assert cache.get_items() == expected_items, "Cache does not contain the expected items after exceeding max size."


def test_undo():
    """
    Test the undo functionality.
    """
    cache = FameSessionCache()
    for i in range(5):
        cache.add_item(create_item(i))

    undone_item = cache.get_last_item()
    assert undone_item == create_item(4), "Undo did not return the correct item."
    assert len(cache.get_items()) == 4, "Item was not removed from the cache after undo."
    assert len(cache.redo_items) == 1, "Undo did not add the item to redo_items."


def test_redo():
    """
    Test the redo functionality after an undo.
    """
    cache = FameSessionCache()
    for i in range(3):
        cache.add_item(create_item(i))

    undone_item = cache.get_last_item()
    assert undone_item == create_item(2), "Undo did not return the correct item."

    redone_item = cache.redo_last_item()
    assert redone_item == create_item(2), "Redo did not return the correct item."
    assert len(cache.get_items()) == 3, "Item was not re-added to the cache after redo."
    assert len(cache.redo_items) == 0, "Redo did not remove the item from redo_items."


def test_clear_redo_stack_on_new_addition():
    """
    Ensure that the redo stack is cleared when a new item is added after an undo.
    """
    cache = FameSessionCache()
    cache.add_item(create_item(1))
    cache.add_item(create_item(2))

    # Perform undo
    undone_item = cache.get_last_item()
    assert undone_item == create_item(2), "Undo did not return the correct item."
    assert len(cache.redo_items) == 1, "Undo did not add the item to redo_items."

    # Add a new item
    cache.add_item(create_item(3))
    assert len(cache.redo_items) == 0, "Redo stack was not cleared after adding a new item."


def test_remove_item_by_index():
    """
    Test removing an item by index.
    """
    cache = FameSessionCache()
    items = [create_item(i) for i in range(3)]
    for item in items:
        cache.add_item(item)

    removed_item = cache.remove_item_by_index(1)
    assert removed_item == create_item(1), "Incorrect item was removed by index."
    assert len(cache.get_items()) == 2, "Item was not removed correctly."
    assert cache.get_items() == [create_item(0), create_item(2)], "Cache items do not match expected after removal."


def test_get_items():
    """
    Test retrieving the current list of items.
    """
    cache = FameSessionCache()
    items = [create_item(i) for i in range(5)]
    for item in items:
        cache.add_item(item)

    retrieved_items = cache.get_items()
    assert retrieved_items == items, "Retrieved items do not match the added items."


def test_get_last_item_empty_cache():
    """
    Test getting the last item from an empty cache.
    """
    cache = FameSessionCache()
    last_item = cache.get_last_item()
    assert last_item is None, "get_last_item should return None when cache is empty."


def test_redo_without_undo():
    """
    Test that redo does nothing if no undo has been performed.
    """
    cache = FameSessionCache()
    cache.add_item(create_item(1))
    redone_item = cache.redo_last_item()
    assert redone_item is None, "Redo should return None when there is nothing to redo."
    assert len(cache.get_items()) == 1, "Cache should remain unchanged when redo is not possible."


def test_undo_until_empty():
    """
    Test undoing all items until the cache is empty.
    """
    cache = FameSessionCache()
    items = [create_item(i) for i in range(3)]
    for item in items:
        cache.add_item(item)

    for i in reversed(range(3)):
        undone_item = cache.get_last_item()
        assert undone_item == items[i], f"Undo did not return the correct item {i}."

    assert len(cache.get_items()) == 0, "Cache should be empty after undoing all items."
    assert len(cache.redo_items) == 3, "All undone items should be in redo_items."


def test_redo_after_multiple_undos():
    """
    Test performing multiple undos followed by redos.
    """
    cache = FameSessionCache()
    items = [create_item(i) for i in range(5)]
    for item in items:
        cache.add_item(item)

    # Perform two undos
    undone_item1 = cache.get_last_item()
    undone_item2 = cache.get_last_item()
    assert undone_item1 == items[4], "First undo did not return the correct item."
    assert undone_item2 == items[3], "Second undo did not return the correct item."

    # Perform two redos
    redone_item1 = cache.redo_last_item()
    redone_item2 = cache.redo_last_item()
    assert redone_item1 == items[3], "First redo did not return the correct item."
    assert redone_item2 == items[4], "Second redo did not return the correct item."
    assert len(cache.get_items()) == 5, "Cache should have all items after redos."
    assert len(cache.redo_items) == 0, "Redo stack should be empty after all redos."


def test_add_non_dict_item():
    """
    Test that adding a non-dictionary item raises a ValueError.
    """
    cache = FameSessionCache()
    with pytest.raises(ValueError):
        cache.add_item(["not", "a", "dict"])
