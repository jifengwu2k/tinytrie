# TinyTrie

A minimal and type-safe trie (prefix tree) implementation for Python 3.6+.

TinyTrie provides basic operations on Tries:
- Insertion of sequences (`search_or_create`)
- Search for sequences (`search`)
- Find the longest common prefix (`longest_common_prefix`)
- Collect all stored sequences (`collect_sequences`)

It supports any type of keys and values using Python's type hints.

## Features

- **Typed**: Works with arbitrary key and value types (`Generic[K, V]`)
- **Minimal**: Only essential functionalities
- **Efficient**: Memory-efficient with `__slots__`
- **Iterable**: Easily traverse and list all stored sequences
- **No external dependencies**

## Example Usage

```python
from tinytrie import TrieNode, search, search_or_create, longest_common_prefix, collect_sequences

# Create the root node
root = TrieNode[str, int]()

# Insert sequences
search_or_create(root, ['a', 'b', 'c'], value=1)
search_or_create(root, ['a', 'b', 'd'], value=2)

# Search for a sequence
node = search(root, ['a', 'b', 'c'])
if node is not None:
    print(f"Found with value: {node.value}")

# Find the longest common prefix
prefix, node = longest_common_prefix(root)
print(f"Longest common prefix: {prefix}")

# Collect all sequences
for seq, node in collect_sequences(root):
    print(f"Sequence: {seq}, Value: {node.value}")
```

Output:

```
Found with value: 1
Longest common prefix: ['a', 'b']
Sequence: ['a', 'b', 'c'], Value: 1
Sequence: ['a', 'b', 'd'], Value: 2
```

## Installation


```bash
pip install tinytrie
```

## License

MIT License