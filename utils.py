import os.path
import sys
import concurrent.futures as cf
from functools import wraps


def resourcePath(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def setLabel(language, polish, english):
    if language == 'polish':
        return polish
    return english


_DEFAULT_POOL = cf.ThreadPoolExecutor()


def threadpool(f, executor=None):
    @wraps(f)
    def wrap(*args, **kwargs):
        return (executor or _DEFAULT_POOL).submit(f, *args, **kwargs)
    return wrap

def addZero(s):
    if len(s) == 1:
        return '0' + s
    return s

if __name__ == '__main__':
    pass
