import argparse
import logging
import deflate.errors as errors
from deflate.handlers.compressor import Compressor
from deflate.handlers.decompressor import Decompressor


def compress(path: str, archive_name: str):
    compressor = Compressor()
    data_to_decode = compressor.read_from_file(path)
    encoded_data, time = compressor.compress(data_to_decode, path)
    compressor.write_archive(archive_name, encoded_data)
    compress_ratio = compressor.calculate_compress_ratio(len(data_to_decode),
                                                         len(encoded_data))
    print(f'Compress ratio: {compress_ratio}%\n'
          f'Time: {time}\n'
          f'Checksum: {compressor.checksum.hex()}\n'
          f'Archive successfully created')


def decode(path: str):
    decompressor = Decompressor()
    data = decompressor.read_from_archive(path)
    file, decoded_data = decompressor.decompress(data)
    decompressor.write_file(file, decoded_data)
    print('Archive successfully decompressed')


def create_cmd_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', default=None,
                        help='path to file')
    parser.add_argument('-d', '--decode', action='store_true', dest='decode',
                        help='to decode file')
    parser.add_argument('-n', '--name', default="", dest='name',
                        help='to set name for archive')

    return parser


if __name__ == '__main__':
    cmd_parser = create_cmd_parser()
    args = cmd_parser.parse_args()
    try:
        if args.decode:
            decode(args.path)
        else:
            compress(args.path, args.name)
    except errors.DeflateError as e:
        logging.basicConfig(level=logging.INFO)
        logging.error(e.message)
        exit(1)
