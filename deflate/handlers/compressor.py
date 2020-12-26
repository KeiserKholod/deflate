import json
import struct
import time
from datetime import datetime
from pathlib import Path
from bitarray import bitarray
from deflate.huffman import HuffmanCodec
from deflate.lz77 import LZ77Codec


class TimeMeasure:
    """Context manager for compressing duration measuring."""

    def __init__(self):
        self.start_time = 0
        self.work_time = 0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.work_time = time.perf_counter() - self.start_time


class Compressor:
    """
    Handler for compress data with deflate algorithm.
    Contain methods to calculate compress ratio,
    read data from file and
    create new archive in File system.
    """

    def compress(self, data: bytes, filename: str) -> tuple:
        """
        Compress bin data with deflate algorithm.
        At first, compress data with LZ77 and then with huffman.
        """

        with TimeMeasure() as measure:
            compressed_data = bytearray()
            lz77_codec = LZ77Codec(256)
            huffman_codec = HuffmanCodec()
            checksum = huffman_codec.get_checksum(data)
            codewords = lz77_codec.encode(data)
            codewords_bytes = b''
            for codeword in codewords:
                codewords_bytes += bytes([codeword.offset])
                codewords_bytes += bytes([codeword.length])
                codewords_bytes += bytes([codeword.char])
            encoded_data, codes_table = huffman_codec.encode(codewords_bytes)
            packed_data = self._pack_data(encoded_data, checksum, codes_table)
            compressed_data.extend(struct.pack('H', len(filename)))
            compressed_data.extend(filename.encode())
            compressed_data.extend(packed_data)

        time_duration = measure.work_time
        return compressed_data, time_duration

    @staticmethod
    def calculate_compress_ratio(original_size, compressed_size) -> float:
        """
        Calculate compress ratio.
        Can be < 0, if file is already compressed or is too small.
        """

        return (1 - compressed_size / original_size) * 100

    @staticmethod
    def _pack_data(encoded_data: bitarray, checksum: bytes,
                   codes_table: dict) -> bytes:
        """
        Pack encoded data to write in file.
        Needs because in LZ77 we use Codewords instead of bytes.
        """

        packed_data = bytearray()
        packed_data.extend(checksum)
        serialized_table = json.dumps({int(i): codes_table[i].to01()
                                       for i in codes_table}).encode()
        packed_data.extend(struct.pack('I', len(serialized_table)))
        packed_data.extend(serialized_table)
        packed_data.extend(struct.pack('I', len(encoded_data)))
        packed_data.extend(encoded_data.tobytes())
        return bytes(packed_data)

    @staticmethod
    def read_from_file(filename: str) -> bytes:
        """Read bin data from file."""

        file = Path.cwd() / filename
        return file.read_bytes()

    @staticmethod
    def write_archive(archive_name: str, encoded_data: bytes) -> None:
        """Get name for archive and save it in file system."""

        if not archive_name:
            archive_name = f'archived by deflate at' \
                           f' {datetime.today().strftime("%Y-%m-%d")}.dfa'
        else:
            archive_name = ''.join((archive_name, '.dfa'))
        archive_path = Path.cwd() / archive_name
        data_to_archive = bytearray(encoded_data)
        archive_path.write_bytes(data_to_archive)
