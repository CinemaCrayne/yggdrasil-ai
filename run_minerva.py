import builtins
import functools

# Patch open() to default to UTF-8 for writing text
_original_open = open

@functools.wraps(_original_open)
def utf8_open(*args, **kwargs):
    if 'encoding' not in kwargs and 'b' not in kwargs.get('mode', ''):
        kwargs['encoding'] = 'utf-8'
    return _original_open(*args, **kwargs)

builtins.open = utf8_open

from yggdrasil_ai.minerva_loop import minerva_reflection_loop
from dotenv import load_dotenv; load_dotenv()

if __name__ == "__main__":
    print("[FILE] Starting Minerva loop...")
    minerva_reflection_loop()
