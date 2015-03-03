import hashlib

__author__ = 'snorri.sturluson'


def calc_checksum(filename):
    """
    Calculates a checksum of the contents of the given file.
    :param filename:
    :return:
    """
    try:
        f = open(filename, "rb")
        contents = f.read()
        m = hashlib.md5()
        m.update(contents)
        checksum = m.hexdigest()
        return checksum

    except IOError:
        return None