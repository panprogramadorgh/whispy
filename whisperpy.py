import os
from typing import Optional 
import ctypes

# _libc = ctypes.CDLL("libc.so.6")
# _libc.malloc.argtypes = [c_uint64]
# _libc.malloc.restype = [c_void_p]
# _libc.free.argtypes = [c_void_p]
# _libc.free.restype = None

_libwhisperpy = ctypes.CDLL("./build/libwhisperpy.so")
_libwhisperpy.init_model_context.argtypes = [ctypes.c_char_p]
_libwhisperpy.init_model_context.restype = ctypes.c_int

class WhisperModel:
  def __init__(self, model_path: str):
    ret = _libwhisperpy.init_model_context(bytes(model_path, encoding="utf-8"))
    if ret > 0:
      raise RuntimeError("Failed to load whisper model.")

def main():
  pass
if __name__ == "__main__":
  main()