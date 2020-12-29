from typing import List, Sequence
from deflate import errors


class Codeword:
    """
    Codeword for LZ77 algorithm.
    Contains length of codeword, offset and code of char.
    Can be compared.
    """

    def __init__(self, offset: int = 0,
                 length: int = 0,
                 char: int = 0):
        self.offset = offset
        self.length = length
        self.char = char

    def __len__(self):
        # т.к в кодовом словаре на один символ больше
        return self.length + 1

    def __eq__(self, other):
        if isinstance(other, Sequence):
            return self.offset == other[0] \
                   and self.length == other[1] \
                   and self.char == other[2]
        else:
            return self.offset == other.offset \
                   and self.length == other.length \
                   and self.char == other.char


class LZ77Codec:
    """
    Contain methods to encode and decode bin data with LZ77 algorithm.
    Requires size of sliding window.
    """

    def __init__(self, window_length):
        self.window_length = window_length
        self.buffer = None

    def encode(self, data: bytes) -> list:
        """
        Encode bin data with LZ77 algorithm.
        Return list of Codewords
        """

        self.buffer = data
        encoded_data = []
        position = 0
        while position < len(data):
            codeword = self.codeword_for_position(position)
            position += len(codeword)
            while codeword.length > self.window_length:
                codeword_split = Codeword(codeword.offset,
                                          self.window_length - 1,
                                          codeword.char)
                codeword = Codeword(codeword.offset + 1,
                                    codeword.length -
                                    self.window_length,
                                    codeword.char)
                encoded_data.append(codeword_split)
                continue
            encoded_data.append(codeword)
        return encoded_data

    def codeword_for_position(self, position: int) -> Codeword:
        """Get codeword with position of sequence."""

        longest_match_length = 0
        longest_match_offset = 0
        start_offset = 1
        start_position = position - start_offset

        while start_offset < self.window_length and start_position >= 0:
            match_length = self.get_max_match_len(start_position, position)
            if match_length > longest_match_length:
                longest_match_length = match_length
                longest_match_offset = start_offset
            start_position -= 1
            start_offset += 1

        return Codeword(longest_match_offset, longest_match_length,
                        self.buffer[position + longest_match_length])

    def get_max_match_len(self, pattern_position: int, matching_position: int) -> int:
        """Get length of max substring."""

        match_length = 0
        while matching_position + match_length + 1 < len(self.buffer):
            if self.buffer[pattern_position + match_length] != \
                    self.buffer[matching_position + match_length]:
                break
            match_length += 1
        return match_length

    @staticmethod
    def decode(codewords: List[Codeword]) -> bytes:
        """Get decoded bin data by list of codewords."""

        buffer = bytes()
        for codeword in codewords:
            if codeword.offset > len(buffer):
                raise errors.CodewordNotInWindowError()
            elif codeword.offset < 0:
                raise errors.CodewordOffsetNegativeError()
            elif codeword.offset > 0:
                position = len(buffer) - codeword.offset
                for i in range(codeword.length):
                    buffer += bytes([buffer[position]])
                    position += 1
            buffer += bytes([codeword.char])
        return buffer
