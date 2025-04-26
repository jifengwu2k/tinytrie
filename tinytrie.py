# tinytrie: A minimal and type-safe trie (prefix tree) implementation in Python.
# Copyright (c) 2025 Jifeng Wu
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
from typing import TypeVar, Generic, Dict, Optional, Sequence, List, Tuple, Iterator


__all__ = [
    "TrieNode",
    "search",
    "search_or_create",
    "longest_common_prefix",
    "collect_sequences",
]


K = TypeVar("K")
V = TypeVar("V")


class TrieNode(Generic[K, V]):
    __slots__ = ("children", "is_end", "value")

    children: Dict[K, "TrieNode[K, V]"]
    is_end: bool
    value: Optional[V]

    def __init__(self):
        self.children = {}
        self.is_end = False
        self.value = None


def search(root: TrieNode[K, V], sequence: Sequence[K]) -> Optional[TrieNode[K, V]]:
    if not sequence:
        return root if root.is_end else None
    first, remaining = sequence[0], sequence[1:]
    if first not in root.children:
        return None
    return search(root.children[first], remaining)


def search_or_create(
    root: TrieNode[K, V], sequence: Sequence[K], value: Optional[V] = None
) -> TrieNode[K, V]:
    if not sequence:
        if not root.is_end:
            root.is_end = True
            root.value = value
        return root
    first, remaining = sequence[0], sequence[1:]
    if first not in root.children:
        root.children[first] = TrieNode()
    return search_or_create(root.children[first], remaining, value)


def longest_common_prefix(root: TrieNode[K, V]) -> Tuple[Sequence[K], TrieNode[K, V]]:
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


def collect_sequences(
    root: TrieNode[K, V], prefix: Optional[List[K]] = None
) -> Iterator[Tuple[List[K], TrieNode[K, V]]]:
    if prefix is None:
        prefix = []

    if root.is_end:
        yield prefix.copy(), root

    for key, child in root.children.items():
        prefix.append(key)
        yield from collect_sequences(child, prefix)
        prefix.pop()
