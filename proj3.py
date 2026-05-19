from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(order=True, frozen=True)
class Node:
    freq: int
    char: str
    left: "Node | None" = None
    right: "Node | None" = None

    def __str__(self):
        return f"Node: {self.char}, Freq: {self.freq}"

@dataclass(frozen=True)
class MinHeap:
    data: list[Node] = field(default_factory=list)


def heapify_up(heap: MinHeap, index: int) -> MinHeap:
    data = heap.data[:]

    while index > 0:
        parent = (index - 1) // 2

        if data[index] < data[parent]:
            data[index], data[parent] = data[parent], data[index]
            index = parent
        else:
            break

    return MinHeap(data)


def insert(heap: MinHeap, element: Node) -> MinHeap:
    new_heap = MinHeap(heap.data + [element])

    return heapify_up(new_heap, len(new_heap.data) - 1)


def heapify_down(heap: MinHeap, index: int) -> MinHeap:
    data = heap.data[:]
    size = len(data)

    while True:
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index

        if left < size and data[left] < data[smallest]:
            smallest = left

        if right < size and data[right] < data[smallest]:
            smallest = right

        if smallest != index:
            data[index], data[smallest] = data[smallest], data[index]
            index = smallest
        else:
            break

    return MinHeap(data)


def extract_min(heap: MinHeap) -> tuple[MinHeap, Node]:
    minimum = heap.data[0]

    if len(heap.data) == 1:
        return MinHeap([]), minimum

    new_data = [heap.data[-1]] + heap.data[1:-1]

    new_heap = MinHeap(new_data)

    return heapify_down(new_heap, 0), minimum


def count_frequency(s: str) -> dict[str, int]:
    freq = {}

    for char in s:
        freq[char] = freq.get(char, 0) + 1

    return freq


def create_priority_queue(frequency: dict[str, int]) -> MinHeap:
    heap = MinHeap([])

    for char, freq in frequency.items():
        heap = insert(heap, Node(freq, char))

    return heap


def build_tree(priority_queue: MinHeap) -> Node:
    heap = priority_queue

    while len(heap.data) > 1:
        heap, left = extract_min(heap)
        heap, right = extract_min(heap)

        merged = Node(
            left.freq + right.freq,
            min(left.char, right.char),
            left,
            right
        )

        heap = insert(heap, merged)

    return heap.data[0]


def generate_codes(node: Node | None, prefix="", code: dict | None = None) -> dict:
    if code is None:
        code = {}

    if node is None:
        return code

    if node.left is None and node.right is None:
        code[node.char] = prefix or "0"
        return code

    generate_codes(node.left, prefix + "0", code)
    generate_codes(node.right, prefix + "1", code)

    return code


def encode(s: str, codes: dict) -> str:
    return "".join(codes[char] for char in s)


def decode(encoded_string: str, root: Node):
    if root.left is None and root.right is None:
        return root.char * len(encoded_string)

    decoded = ""
    current = root

    for bit in encoded_string:
        if bit == "0":
            current = current.left
        else:
            current = current.right

        if current.left is None and current.right is None:
            decoded += current.char
            current = root

    return decoded


def huffman_encoding(s: str):
    # Do Not Change this function
    frequency = count_frequency(s)
    pq = create_priority_queue(frequency)

    root = build_tree(pq)

    codes = generate_codes(root)
    encoded_string = encode(s, codes)
    decoded_string = decode(encoded_string, root)

    return encoded_string, decoded_string, codes