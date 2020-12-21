import argparse
import logging


def create_cmd_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', default=None,
                        help='path to file')
    parser.add_argument('-d', '--decode', action='store_true', dest='decode',
                        help='to decode file')

    return parser


if __name__ == '__main__':
    cmd_parser = create_cmd_parser()
    args = cmd_parser.parse_args()
