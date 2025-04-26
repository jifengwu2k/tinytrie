import unittest
from tinytrie import *

class TestTrie(unittest.TestCase):
    def test_insert_and_search(self):
        root = TrieNode[str, str]()
        inserted = search_or_create(root, ['a', 'b', 'c'], value="abc")
        self.assertTrue(inserted.is_end)
        self.assertEqual(inserted.value, "abc")

        found = search(root, ['a', 'b', 'c'])
        self.assertIsNotNone(found)
        self.assertEqual(found.value, "abc")

    def test_search_missing(self):
        root = TrieNode[str, str]()
        search_or_create(root, ['x', 'y', 'z'], value="xyz")

        missing = search(root, ['a', 'b', 'c'])
        self.assertIsNone(missing)

    def test_partial_insert(self):
        root = TrieNode[str, int]()
        search_or_create(root, ['a', 'b'], value=12)

        partial = search(root, ['a'])
        self.assertIsNone(partial)

        full = search(root, ['a', 'b'])
        self.assertIsNotNone(full)
        self.assertEqual(full.value, 12)

    def test_multiple_inserts(self):
        root = TrieNode[str, int]()
        search_or_create(root, ['x'], value=1)
        search_or_create(root, ['x', 'y'], value=2)
        search_or_create(root, ['x', 'y', 'z'], value=3)

        self.assertEqual(search(root, ['x']).value, 1)
        self.assertEqual(search(root, ['x', 'y']).value, 2)
        self.assertEqual(search(root, ['x', 'y', 'z']).value, 3)

    def test_longest_common_prefix(self):
        root = TrieNode()
        search_or_create(root, 'flower')
        search_or_create(root, 'flow')
        search_or_create(root, 'flight')
        
        ref_prefix = ['f', 'l']
        
        prefix, _ = longest_common_prefix(root)
        
        self.assertEqual(prefix, ref_prefix)

    def test_collect_sequences(self):
        root = TrieNode[str, str]()
        search_or_create(root, ['a'], value="A")
        search_or_create(root, ['a', 'b'], value="AB")
        search_or_create(root, ['x', 'y', 'z'], value="XYZ")
        sequences = [ (sequence, node.value) for sequence, node in collect_sequences(root) ]
        expected = [
            (['a'], "A"),
            (['a', 'b'], "AB"),
            (['x', 'y', 'z'], "XYZ")
        ]
        self.assertCountEqual(sequences, expected)
    
if __name__ == '__main__':
    unittest.main()
