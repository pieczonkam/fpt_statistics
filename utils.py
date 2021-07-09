import os.path
import sys

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

if __name__ == '__main__':
    pass