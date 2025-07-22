# tinytrie: A minimal and type-safe trie (prefix tree) implementation in Python.
# Copyright (c) 2025 Jifeng Wu
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
from typing import TypeVar, Generic, Dict, Optional, Sequence, List, Tuple, Iterator

K = TypeVar("K")
V = TypeVar("V")


class TrieNode(Generic[K, V]):
    """A node in the trie structure.

    Attributes:
        children: Dictionary mapping keys to child nodes
        is_end: Boolean indicating if this node completes a sequence
        value: Optional value associated with this node if is_end is True"""
    __slots__ = ("children", "is_end", "value")

    def __init__(self):
        self.children = {}  # type: Dict[K, TrieNode[K, V]]

        self.is_end = False  # type: bool
        self.value = None  # type: Optional[V]


def get_subtrie_root(root, sequence, index=0):
    """Get the root of a subtrie.

    Args:
        root: Root node of the trie
        sequence: Sequence of keys to search for
        index: Current index in sequence (used internally for recursion)

    Returns:
        The node if found, None otherwise

    Time complexity: O(n) where n is length of sequence"""
    if index >= len(sequence):
        return root
    else:
        key = sequence[index]
        if key not in root.children:
            return None
        else:
            return get_subtrie_root(root.children[key], sequence, index + 1)


def search(root, sequence):
    # type: (TrieNode[K, V], Sequence[K]) -> Optional[TrieNode[K, V]]
    """Search for a sequence stored in the trie.

    Args:
        root: Root node of the trie
        sequence: Sequence of keys to search for

    Returns:
        The terminal node if found, None otherwise

    Time complexity: O(n) where n is length of sequence"""
    subtrie = get_subtrie_root(root, sequence)
    if subtrie is not None:
        # Is the sequence stored in the tree?
        if not subtrie.is_end:
            return None
    return subtrie


def update(root, sequence, value=None, index=0):
    # type: (TrieNode[K, V], Sequence[K], Optional[V], int) -> TrieNode[K, V]
    """Search for a sequence, creating nodes if not found, and set a value for the terminal node.

    Args:
        root: Root node of the trie
        sequence: Sequence of keys to insert
        value: Value to associate with the terminal node
        index: Current index in sequence (used internally for recursion)

    Returns:
        The terminal node for the sequence

    Time complexity: O(n) where n is length of sequence"""
    if index >= len(sequence):
        if not root.is_end:
            root.is_end = True

        root.value = value
        return root
    else:
        key = sequence[index]
        if key not in root.children:
            root.children[key] = TrieNode()
        return update(root.children[key], sequence, value, index + 1)


def delete(root, sequence, index=0):
    # type: (TrieNode[K, V], Sequence[K], int) -> bool
    """Delete a sequence from the trie.

    Args:
        root: Root node of the trie
        sequence: Sequence to delete
        index: Current index in sequence (used internally for recursion)

    Returns:
        True if sequence was found and deleted, False otherwise

    Time complexity: O(n) where n is length of sequence"""
    if index >= len(sequence):
        if not root.is_end:
            return False  # Sequence not found
        else:
            root.is_end = False
            root.value = None
            return True  # Sequence found and marked as deleted
    else:
        key = sequence[index]
        if key not in root.children:
            return False  # Sequence not found
        else:
            child = root.children[key]
            deleted = delete(child, sequence, index + 1)

        if not deleted:
            return False
        else:
            # Prune the child if it's now a leaf node and not a terminal
            if not child.is_end and not child.children:
                del root.children[key]

            return True


def longest_common_prefix(root):
    # type: (TrieNode[K, V]) -> Tuple[Sequence[K], TrieNode[K, V]]
    """Find the longest sequence that is a prefix of all sequences in the trie.

    Args:
        root: Root node of the trie

    Returns:
        Tuple of (prefix sequence, terminal node)

    Time complexity: O(m) where m is length of longest common prefix"""
    prefix = []
    node = root

    while True:
        # Stop if node is end of word or has multiple children
        if node.is_end or len(node.children) != 1:
            break
        # Get the only child
        key, next_node = next(iter(node.children.items()))
        prefix.append(key)
        node = next_node

    return prefix, node


def collect_sequences(root, prefix=None):
    # type: (TrieNode[K, V], Optional[List[K]]) -> Iterator[Tuple[List[K], TrieNode[K, V]]]
    """Generate all sequences stored in the trie.
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
