class DeflateError(Exception):
    message = "Error"


class WrongChecksumError(DeflateError):
    message = 'Wrong chesksum'


class CodewordNotInWindowError(DeflateError):
    message = 'Codeword not in window, file can not be  decompressed'


class CodewordOffsetNegativeError(DeflateError):
    message = 'Codeword offset negative, file can not be decompressed'


class NotArchiveError(DeflateError):
    message = 'File extension is not .dfa'


class BrokenArchiveError(DeflateError):
    message = 'Can not decode data'
