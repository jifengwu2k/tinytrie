# TinyTrie

A minimal and type-safe trie (prefix tree) implementation for Python 2+.

## Features

- **Typed**: Works with arbitrary key and value types (`Generic[K, V]`)
- **Minimal**: Only essential functionalities
- **Efficient**: Memory-efficient with `__slots__`
- **Iterable**: Easily traverse and list all stored sequences
- **No external dependencies** (except `typing` on Python <3.5)

## Basic Operations

```python 
from tinytrie import *

# Create a trie with character (`str`) keys and integer values
root = TrieNode[str, int]()

# Insert some words with values
update(root, "apple", 1)
update(root, "app", 2)
update(root, "banana", 3)
update(root, "band", 4)

# Search for existing words
assert search(root, "apple").value == 1
assert search(root, "app").value == 2
assert search(root, "banana").value == 3

# Search for non-existent words
assert search(root, "orange") is None
assert search(root, "appetizer") is None

update(root, "apple", 10)
assert search(root, "apple").value == 10  # Value updated

# Insert a new word
update(root, "orange", 5)
assert search(root, "orange").value == 5

# Delete "apple", "app" remains
assert delete(root, "apple") is True
assert search(root, "apple") is None
assert delete(root, "apple") is False
assert search(root, "app") is not None

# Add back "apple", delete "app", "apple" remains
update(root, "apple", 10)
assert delete(root, "app") is True
assert search(root, "app") is None
assert delete(root, "app") is False
assert search(root, "apple") is not None

# Try to delete non-existent words
assert delete(root, "ban") is False
assert delete(root, "appetizer") is False

# Get common prefix from root (no common prefix)
prefix, node = longest_common_prefix(root)
assert prefix == []  # No common prefix among all words

# Get common prefix from "b" subtree
prefix, node = longest_common_prefix(root.children["b"])
assert prefix == ["a", "n"]  # Common between "banana" and "band" after "b"


# Get all words in the trie
words = ["".join(s) for s, _ in collect_sequences(root)]
assert set(words) == {"apple", "banana", "band", "orange"}
```

## Non-String Keys Example

```python
from tinytrie import *

# Create a trie with tuple keys
trajectory_trie = TrieNode[Tuple[int, int], str]()
update(trajectory_trie, [(1,2), (3,4)], "traj1")
update(trajectory_trie, [(1,2), (5,6)], "traj2")

assert search(trajectory_trie, [(1,2), (3,4)]).value == "traj1"
assert search(trajectory_trie, [(1,2), (5,6)]).value == "traj2"
assert search(trajectory_trie, [(1,2)]) is None  # Partial path

prefix, _ = longest_common_prefix(trajectory_trie)
assert prefix == [(1, 2)]
```

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).
