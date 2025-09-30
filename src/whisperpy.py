import ctypes

# User defined types

class _TranscriptContext(ctypes.Structure):
  _fields_ = [
    ("last_error", ctypes.c_uint8),
    ("last_error_message", ctypes.c_char_p),
    ("model_context", ctypes.c_void_p)
  ]

# Function prototyping

_libwhisperpy = ctypes.CDLL("./build/libwhisperpy.so")

_libwhisperpy.transcript_context_make.argtypes = [ctypes.POINTER(_TranscriptContext), ctypes.c_char_p]
_libwhisperpy.transcript_context_make.restype = ctypes.c_uint8

_libwhisperpy.transcript_context_free.argtypes = [ctypes.POINTER(_TranscriptContext)]
_libwhisperpy.transcript_context_free.restype = ctypes.c_uint8

_libwhisperpy.speach_to_text.argtypes = [ctypes.c_char_p, ctypes.c_uint64, ctypes.POINTER(_TranscriptContext), ctypes.c_char_p]
_libwhisperpy.speach_to_text.restype = ctypes.c_uint8

# Internal utils

def _format_tc_error(tc: _TranscriptContext, context: str | None = None):
  message = ""
  if context is not None:
    message += f"{context}: "

  if tc.last_error != 0:
    message += str(tc.last_error_message, encoding="utf-8", errors="#")

  last_error = int(tc.last_error)
  message += f" ({last_error})"
  
  return message

# FIXME: We do not want relative paths here 
_MODELS = {
  "base": b"./src/backend/whisper.cpp/models/ggml-base.bin"
}

def _fetch_model_path(name: str):
  return _MODELS.get(name)

# API

class WhisperInitError(RuntimeError):
  def __init__(self, detail: str | None):
    super().__init__(detail)

class WhisperTextGenError(RuntimeError):
  def __init__(self, detail: str | None):
    super().__init__(detail)


# TODO: Select model name istead of the path
class WhisperModel:
  """
  A python wrapper class over the whisper.cpp library.
  """
  def __init__(self, model_name: str):
    """_summary_

    Args:
        model_path: Anything used to construct a utf-8 bytes object.

    Raises:
        RuntimeError: If the underlying C api detects an error.
    """
    model_path = _fetch_model_path(model_name)
    if model_path is None:
      raise WhisperInitError("No such model name.")

    self._tc = _TranscriptContext()
    make_result = _libwhisperpy.transcript_context_make(ctypes.pointer(self._tc), model_path)
    if make_result != 0:
      raise WhisperInitError(_format_tc_error(self._tc, "Model initialization error"))
  
  def speach_to_text(self, speach_path: str, max_text_size: int = (1 << 10) * 4):
    """Returns a string with the transcription of the speach.

    Args:
        speach_path: Anythin used to construct a utf-8 bytes object. 
    """
    text = (ctypes.c_char * max_text_size)()

    speach_result = _libwhisperpy.speach_to_text(text, max_text_size, self._tc, bytes(speach_path, encoding="utf-8"))
    if speach_result != 0:
      raise WhisperTextGenError(_format_tc_error(self._tc, "Speach to text error"))

    return str(memoryview(text), encoding="utf-8")


def main():
  pass
if __name__ == "__main__":
  main()