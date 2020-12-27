import unittest
from bitarray import bitarray
from deflate.codecs.huffman import HuffmanCodec, Node
from deflate.codecs.lz77 import LZ77Codec, Codeword
import tempfile
from deflate.handlers.compressor import Compressor
from deflate.handlers.decompressor import Decompressor
from pathlib import Path


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


class TestCompressor(unittest.TestCase):
    def test_compressor_read_from_file(self):
        compressor = Compressor()
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
            file.write('wewqtqrtertwerete')
        file_name = file.name
        data_from_file = compressor.read_from_file(file_name)
        self.assertIsNotNone(data_from_file)

    def test_compress_and_decompress_file(self):
        compressor = Compressor()
        decompressor = Decompressor()

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
            file.write('wewqtqrtertwerete')
        file_name = file.name
        archive_name = "qwerty"

        data_from_file = compressor.read_from_file(file_name)

        encoded_data = compressor.compress(data_from_file, file_name)[0]
        compressor.write_archive("qwerty", encoded_data)
        archive = Path.cwd() / (archive_name + '.dfa')

        data_to_decode = decompressor.read_from_archive(archive_name + '.dfa')

        file, decoded_data = decompressor.decompress(data_to_decode)
        decompressor.write_file(file, decoded_data)
        self.assertEqual(decoded_data, data_from_file)
        self.assertIsNotNone(data_to_decode)
        archive.unlink()
