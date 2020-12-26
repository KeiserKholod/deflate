import unittest
from bitarray import bitarray
from deflate.huffman import HuffmanCodec, Node
from deflate.lz77 import LZ77Codec, Codeword


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


class TestLZ77(unittest.TestCase):
    def test_encode(self):
        data = b'ababababababab'
        expected_data = [Codeword(0, 0, 97),
                         Codeword(0, 0, 98),
                         Codeword(2, 11, 98)]
        lz77_codec = LZ77Codec(len(data))
        encoded = lz77_codec.encode(data)
        self.assertEqual(expected_data, encoded)

    def test_encode_large(self):
        data = b'ababababababab' * 10
        expected_data = [Codeword(0, 0, 97),
                         Codeword(0, 0, 98),
                         Codeword(2, 137, 98)]
        lz77_codec = LZ77Codec(len(data))
        encoded = lz77_codec.encode(data)
        i = 0
        for codeword in encoded:
            self.assertEqual(expected_data[i].length, codeword.length)
            self.assertEqual(expected_data[i].char, codeword.char)
            self.assertEqual(expected_data[i].offset, codeword.offset)
            i += 1

    def test_decode(self):
        expected_data = b'ababababababab'
        data = [Codeword(0, 0, 97),
                Codeword(0, 0, 98),
                Codeword(2, 11, 98)]
        lz77_codec = LZ77Codec(len(data))
        decoded = lz77_codec.decode(data)
        self.assertEqual(expected_data, decoded)

    def test_decode_large(self):
        expected_data = b'ababababababab' * 10
        data = [Codeword(0, 0, 97),
                Codeword(0, 0, 98),
                Codeword(2, 137, 98)]
        lz77_codec = LZ77Codec(len(data))
        decoded = lz77_codec.decode(data)
        self.assertEqual(expected_data, decoded)
