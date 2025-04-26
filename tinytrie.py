# tinytrie: A minimal and type-safe trie (prefix tree) implementation in Python.
# Copyright (c) 2025, 2026 Jifeng Wu
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
from typing import TypeVar, Generic, Dict, Optional, Sequence, List, Tuple, Iterable, Iterator, Callable

K = TypeVar("K")
V = TypeVar("V")


class TrieNode(Generic[K, V]):
    """A node in the trie structure.

    Attributes:
        is_end: Boolean indicating if this node completes a sequence
        value: Optional value associated with this node if is_end is True"""

    __slots__ = ('parent', 'children', 'is_end', 'value')

    def __init__(self):
        self.parent = None  # type: Optional[TrieNode[K, V]]
        self.children = {}  # type: Dict[K, TrieNode[K, V]]
        self.is_end = False  # type: bool
        self.value = None  # type: Optional[V]


def traverse(root, path):
    # type: (TrieNode[K, V], Iterable[K]) -> Iterator[Tuple[Optional[TrieNode[K, V]], K]]
    """Traverse the trie following a path of keys, yielding each node and key.

    Args:
        root: Root node of the trie
        path: Path of keys to follow

    Yields:
        Tuples of (node, key) for each step in the traversal. The node will be None
        if the path of keys diverges from the trie structure.

    Note:
        Continues yielding until all keys are exhausted, even if the path diverges
        from the trie structure (in which case subsequent nodes will be None).

    Time complexity: O(n) where n is length of path"""
    node_or_none = root  # type: Optional[TrieNode[K, V]]

    for key in path:
        if node_or_none is not None:
            node_or_none = node_or_none.children.get(key, None)
        yield node_or_none, key


def get_subtrie_root(root, path):
    # type: (TrieNode[K, V], Iterable[K]) -> Optional[TrieNode[K, V]]
    """Get the root node of a subtrie at the end of a path of keys.

    Args:
        root: Root node of the trie
        path: Path of keys to the subtrie

    Returns:
        The node at the end of the path of keys if the full path exists in the trie,
        None otherwise.

    Note:
        Unlike search(), this doesn't check if the node marks the end of a sequence,
        it only verifies the path exists.

    Time complexity: O(n) where n is length of path"""
    subtrie_root = root  # type: TrieNode[K, V]

    for nullable_subtrie_root, _ in traverse(root, path):
        if nullable_subtrie_root is not None:
            subtrie_root = nullable_subtrie_root
        else:
            return None

    return subtrie_root


def search(root, sequence):
    # type: (TrieNode[K, V], Iterable[K]) -> Optional[TrieNode[K, V]]
    """Search for a sequence stored in the trie.

    Args:
        root: Root node of the trie
        sequence: Sequence of keys to search for

    Returns:
        The terminal node if found, None otherwise

    Time complexity: O(n) where n is length of sequence"""
    nullable_subtrie_root = get_subtrie_root(root, sequence)
    if nullable_subtrie_root is not None and nullable_subtrie_root.is_end:
        return nullable_subtrie_root
    else:
        return None


def update(root, sequence, value=None):
    # type: (TrieNode[K, V], Iterable[K], Optional[V]) -> TrieNode[K, V]
    """Update the value of a sequence in the trie. Inserts the sequence into the trie if not already present.

    Args:
        root: Root node of the trie
        sequence: Sequence of keys to insert
        value: Value to associate with the terminal node

    Returns:
        The terminal node for the sequence

    Time complexity: O(n) where n is length of sequence"""
    node = root  # type: TrieNode[K, V]
    for key in sequence:
        if key in node.children:
            child = node.children[key]
        else:
            child = TrieNode()
            node.children[key] = child
            child.parent = node
        node = child
    node.is_end = True
    node.value = value
    return node


def delete_keys_where_value(dictionary, predicate):
    # type: (Dict[K, V], Callable[[V], bool]) -> None
    """Delete keys from a dictionary where the associated value matches a predicate.

    Args:
        dictionary: The dictionary to modify
        predicate: A callable that returns True for values whose keys should be deleted

    Note:
        Modifies the dictionary in-place and does not return anything.
        The predicate is called for each value in the dictionary."""
    keys_to_delete = {key for key, value in dictionary.items() if predicate(value)}
    while keys_to_delete:
        key = keys_to_delete.pop()
        del dictionary[key]


def delete(root, sequence):
    # type: (TrieNode[K, V], Sequence[K]) -> bool
    """Delete a sequence from the trie.

    Args:
        root: Root node of the trie
        sequence: Sequence to delete

    Returns:
        True if sequence was found and deleted, False otherwise

    Time complexity: O(n) where n is length of sequence"""
    nullable_sequence_end_node = search(root, sequence)

    # Did we actually find the sequence?
    if nullable_sequence_end_node is None:
        return False
    else:
        # Mark the sequence as deleted
        nullable_sequence_end_node.is_end = False
        nullable_sequence_end_node.value = None

        # Is the sequence end node in the middle or at the end of a path in the trie?
        # Do cleanup for the latter
        if not nullable_sequence_end_node.children:
            current = nullable_sequence_end_node
            while current is not root:
                parent = current.parent

                # Remove `current` from `parent`
                delete_keys_where_value(parent.children, lambda sibling: sibling is current)

                # If `parent` now has no children and doesn't mark the end of a sequence,
                # recursively delete it
                # Otherwise, we're done
                if parent.children or parent.is_end:
                    break
                else:
                    current = parent

        return True


def longest_common_prefix(root):
    # type: (TrieNode[K, V]) -> Tuple[Sequence[K], TrieNode[K, V]]
    """Find the longest common prefix of all sequences in the trie and its terminal node.

    Args:
        root: Root node of the trie

    Returns:
        Tuple of (prefix, terminal node)

    Time complexity: O(m) where m is length of longest common prefix"""
    prefix = []
    node = root

    while True:
        # Stop if node is end of word or has multiple children
        if node.is_end or len(node.children) != 1:
            break
        else:
            # Get the only child
            key, next_node = next(iter(node.children.items()))
            prefix.append(key)
            node = next_node

    return prefix, node


def collect_sequences(root, prefix=None):
    # type: (TrieNode[K, V], Optional[List[K]]) -> Iterator[Tuple[List[K], TrieNode[K, V]]]
    """Generate all sequences stored in the trie and their terminal nodes.
    Args:
        root: Root node of the trie
        prefix: A prefix to append to the generated sequences

    Yields:
        Tuples of (sequence, terminal node) for all stored sequences

    Time complexity: O(n) per sequence where n is average sequence length"""
    if prefix is None:
        prefix = []

    if root.is_end:
        yield list(prefix), root  # We don't user `list`'s `copy` method because it is not available on Python 2

    for key, child in root.children.items():
        prefix.append(key)
        for _ in collect_sequences(child, prefix):
            yield _
        prefix.pop()
