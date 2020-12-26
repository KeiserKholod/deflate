import heapq
import collections
from hashlib import md5
from bitarray import bitarray
from typing import Optional, DefaultDict


class Node:
    """Node of bin tree for huffman algorithm."""

    def __init__(self, char: int, weight: int,
                 left_child: Optional['Node'] = None,
                 right_child: Optional['Node'] = None):
        self.char = char
        self.weight = weight
        self.left_child = left_child
        self.right_child = right_child
        self.code = -1

    def __lt__(self, other: 'Node'):
        return self.weight < other.weight

    def __eq__(self, other: 'Node'):
        return self.char == other.char and self.code == other.code \
               and self.weight == other.weight


class HuffmanCodec:
    """
    Contain methods for encode and decode bin data
    with huffman algorithm and calculate checksum with md5
    """

    def encode(self, data: bytes) -> tuple:
        """Encode bin data with huffman algorithm."""

        weights_nodes = self.count_frequencies(data)
        tree = self.create_tree(weights_nodes)
        encoded_data, codes_table = self.__encode(tree, data)
        return encoded_data, codes_table

    @staticmethod
    def count_frequencies(data: bytes) -> collections.defaultdict:
        """Calculate weights of current node by freq analysis."""

        weights = collections.defaultdict(int)
        for byte in data:
            weights[byte] += 1
        return weights

    @staticmethod
    def create_tree(weights: DefaultDict) -> heapq:
        """Generate bin tree with Nodes for huffman algorithm."""

        priority_queue = []
        for key in weights:
            heapq.heappush(priority_queue, Node(key, weights[key]))
        while len(priority_queue) > 1:
            left_node = heapq.heappop(priority_queue)
            right_node = heapq.heappop(priority_queue)
            node = Node(left_node.char + right_node.char,
                        left_node.weight + right_node.weight,
                        left_node, right_node)
            left_node.code = 0
            right_node.code = 1
            heapq.heappush(priority_queue, node)
        return heapq.heappop(priority_queue)

    def collect_codes_from_tree(self, tree: Node) -> dict:
        """Get codes of all nodes in bin tree."""

        codes_from_tree = {}
        for byte, code in self.get_code_from_node(tree):
            codes_from_tree[byte] = code
        return codes_from_tree

    def get_code_from_node(self, node: Node,
                           code: tuple = None) -> collections.Iterable:
        """Get Code of the node by other nodes."""

        if not code:
            code = ()
        code_from_node = ()
        if node.code != -1:
            code_from_node = (*code, node.code)
        if not node.right_child and not node.left_child:
            if node.code == -1:
                code_from_node = bitarray([1])
            code_in_bits = bitarray()
            code_in_bits.extend(code_from_node)
            yield node.char, code_in_bits
        else:
            yield from self.get_code_from_node(node.left_child,
                                               code_from_node)
            yield from self.get_code_from_node(node.right_child,
                                               code_from_node)

    def __encode(self, tree: Node, data_to_encode: bytes) -> tuple:
        codes_table = self.collect_codes_from_tree(tree)
        encoded_data = bitarray()
        encoded_data.encode(codes_table, data_to_encode)
        return encoded_data, codes_table

    @staticmethod
    def get_checksum(data: bytes) -> bytes:
        """Get checksum by md5 hash."""

        return md5(data).digest()

    @staticmethod
    def decode(codes_table: dict, encoded_data: bytes,
               skip_length: int) -> bytes:
        """Decode binary data, encoded by huffman algorithm."""

        bit_code_table = {}
        for key in codes_table:
            bits = bitarray()
            for bit in codes_table[key]:
                bits.append(int(bit))
            bit_code_table[int(key)] = bits
        decoded_data = bitarray()
        decoded_data.frombytes(encoded_data)
        decoded_data = decoded_data[:skip_length]
        decoded_data_bytes = bytes(decoded_data.decode(bit_code_table))
        return decoded_data_bytes
