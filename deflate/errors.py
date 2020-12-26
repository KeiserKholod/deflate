class DeflateError(Exception):
    message = "Error"


class WrongChecksumError(Exception):
    message = 'Wrong chesksum'


class CodewordNotInWindowError(Exception):
    message = 'Codeword not in window, file can not be  decompressed'


class CodewordOffsetNegativeError(Exception):
    message = 'Codeword offset negative, file can not be decompressed'


class NotArchiveError(Exception):
    message = 'File extension is not .dfa'


class BrokenArchiveError(Exception):
    message = 'Can not decode data'
