import unittest
from bitarray import bitarray
from deflate.huffman import HuffmanCodec, Node


class TestHuffman(unittest.TestCase):
    def test_encode(self):
        expected_data = bitarray([1, 1, 1, 1, 1])
        huffman_codec = HuffmanCodec()
        result = huffman_codec.encode(b'aaaaa')[0]
        self.assertEqual(expected_data, result)

    def test_decode(self):
        expected_data = b'aaaaa'
        result = HuffmanCodec.decode({97: '1'},
                                     bytes(bitarray([1, 1, 1, 1, 1])),
                                     5)
        self.assertEqual(expected_data, result)

    def test_create_tree(self):
        expected_tree = Node(97, 5)
        huffman_codec = HuffmanCodec()
        freq = huffman_codec.count_frequencies(b'aaaaa')
        tree = huffman_codec.create_tree(freq)
        self.assertEqual(expected_tree, tree)

    def test_checksum(self):
        expected_checksum = b'YO\x80;8\nA9n\xd6=\xca9P5B'
        checksum = HuffmanCodec.get_checksum(b'aaaaa')
        self.assertEqual(expected_checksum, checksum)
