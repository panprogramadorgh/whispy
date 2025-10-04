from os import getenv, path
import ctypes

# Library path

IS_DEVELOPMENT = False
WHISPERPY_LIBRARY_MODE = getenv("WHISPERPY_LIBRARY_MODE")
if WHISPERPY_LIBRARY_MODE and isinstance(WHISPERPY_LIBRARY_MODE, str):
  IS_DEVELOPMENT = WHISPERPY_LIBRARY_MODE.strip().lower().split()[0].startswith("dev")

def get_whisperpy_backend_library_path():
  project_root = path.dirname(path.dirname(__file__))
  backend_dir =  {
    True: path.join(project_root, "cmake-dev-build"), # Is development
    False: path.join(project_root, "cmake-build") # Is not development
  }[IS_DEVELOPMENT]
  backend_lib_path = path.join(backend_dir, "libwhisperpy.so")
  if not path.exists(backend_lib_path):
    raise RuntimeError(f"Unable to find whisperpy backend library: {backend_lib_path}")
  return backend_lib_path

# User-defined types

class TranscriptContext(ctypes.Structure):
  _fields_ = [
    ("last_error_code", ctypes.c_uint8),
    ("last_error_message", ctypes.c_char_p),
    ("model_context", ctypes.c_void_p)
  ]

# Load library (singleton)

libwhisperpy: ctypes.CDLL | None = None
libwhisperpy_ld_error: str | None = None
try:
  libwhisperpy = ctypes.CDLL(get_whisperpy_backend_library_path())
except Exception as error:
  libwhisperpy_ld_error = f"Unable to load whisperpy backend library: {error}"
else:
  libwhisperpy.transcript_context_make.argtypes = [ctypes.POINTER(TranscriptContext), ctypes.c_char_p]
  libwhisperpy.transcript_context_make.restype = ctypes.c_uint8

  libwhisperpy.transcript_context_free.argtypes = [ctypes.POINTER(TranscriptContext)]
  libwhisperpy.transcript_context_free.restype = ctypes.c_uint8

  libwhisperpy.speach_to_text.argtypes = [ctypes.c_char_p, ctypes.c_uint64, ctypes.POINTER(TranscriptContext), ctypes.c_char_p]
  libwhisperpy.speach_to_text.restype = ctypes.c_uint8

class WhisperpyLoader:
  def __init__(self):
    self._lib = libwhisperpy
    self._loading_error = libwhisperpy_ld_error
  
  def get(self):
    if self._loading_error is not None:
      raise RuntimeError(self._loading_error)
    return self._lib

  def __bool__(self):
    self._loading_error is None
  
  def __repr__(self):
    verified_message = self._loading_error if self._loading_error is not None else "no errors"
    return f"< WhisperLoader _loading_error='{verified_message}' >"
  
