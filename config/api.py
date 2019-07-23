import os

WINDOWS_DRIVE = 'Z:/'
UNIX_DRIVE = '/mnt/nas1/'


def drive():
    """
    Check to see if you're running Windows or UNIX system
    and return the server mounting drive file path...
    """

    from platform import system

    if system() == 'Windows':
        return WINDOWS_DRIVE

    else:
        return UNIX_DRIVE


def unix(path):
    return path.replace('\\', '/')


def walk(schema, base=''):
    """
    Run through a dictionary folder scheme and return a joined path...

    :param dict schema:
    :param str base:
    :return generator:
    """
    for key, item in schema.items():
        _key = os.path.join(base, key)
        yield _key

        if isinstance(item, dict):
            for v in walk(item, _key):
                yield v

        elif isinstance(item, list):
            for v in item:
                yield os.path.join(_key, v)

        elif isinstance(item, str):
            yield os.path.join(_key, item)


def find(*args):
    """
    Find the path of listed args...

    :param args:
    :return:
    """

    import config

    for key in args:
        key = unix(key)

        for path in walk(config.server):
            if key.lower() in unix(path.lower()):
                yield unix(path)


if __name__ == '__main__':
    pass