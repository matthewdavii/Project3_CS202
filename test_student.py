import unittest

from proj3 import (
    Node,
    MinHeap,
    insert,
    extract_min,
    count_frequency,
    create_priority_queue,
    build_tree,
    generate_codes,
    encode,
    decode
)


class TestStudent(unittest.TestCase):

    def test_count_frequency(self):
        self.assertEqual(
            count_frequency("aaabbc"),
            {'a': 3, 'b': 2, 'c': 1}
        )

    def test_insert(self):
        heap = MinHeap([])

        heap = insert(heap, Node(5, "a"))
        heap = insert(heap, Node(1, "b"))

        self.assertEqual(heap.data[0].freq, 1)

    def test_extract_min(self):
        heap = MinHeap([])

        heap = insert(heap, Node(3, "a"))
        heap = insert(heap, Node(1, "b"))

        heap, minimum = extract_min(heap)

        self.assertEqual(minimum.freq, 1)

    def test_encode_decode(self):
        s = "hello"

        freq = count_frequency(s)

        pq = create_priority_queue(freq)

        root = build_tree(pq)

        codes = generate_codes(root)

        encoded = encode(s, codes)

        decoded = decode(encoded, root)

        self.assertEqual(decoded, s)


if __name__ == "__main__":
    unittest.main()