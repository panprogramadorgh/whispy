from os import path
import ctypes

# Library path

def get_libwhisperpy_path():
  libwhisperpy_path = path.join(path.dirname(__file__), "lib", "libwhisperpy.so")
  if not path.exists(libwhisperpy_path):
    raise RuntimeError(f"Unable to find whisperpy backend library: {libwhisperpy_path}")
  return libwhisperpy_path

# User-defined types

class TranscriptContext(ctypes.Structure):
  _fields_ = [
    ("last_error_code", ctypes.c_uint8),
    ("last_error_message", ctypes.c_char_p),
    ("model_context", ctypes.c_void_p)
  ]

class DwtAhead(ctypes.Structure):
  _field_ = [
    ("n_text_layer", ctypes.c_int),
    ("n_head", ctypes.c_int)
  ]

class DwtAheads(ctypes.Structure):
  _field_ = [
    ("n_heads", ctypes.c_uint64),
    ("heads", ctypes.POINTER(DwtAhead))
  ]

class WhisperContextParams(ctypes.Structure):
  _fields_ = [
    ("use_gpu", ctypes.c_bool),
    ("flash_attn", ctypes.c_bool),
    ("gpu_device", ctypes.c_int),
    ("dtw_token_timestamps", ctypes.c_bool),
    ("dtw_aheads_preset", ctypes.c_int),
    ("dtw_n_top", ctypes.c_int),
    ("dtw_aheads", DwtAheads),
    ("dtw_mem_size", ctypes.c_uint64)
  ]

class WhisperFullParams(ctypes.Structure):
  _fields = [
    ("strategy", ctypes.c_int),
    ("n_threads", ctypes.c_int),
    ("n_max_text_ctx", ctypes.c_int),
    ("offset_ms", ctypes.c_int),
    ("duration_ms", ctypes.c_int),

    ("translate", ctypes.c_bool),
    ("no_context", ctypes.c_bool),
    ("no_timestampts", ctypes.c_bool),
    ("single_segment", ctypes.c_bool),
    ("print_special", ctypes.c_bool),
    ("print_progress", ctypes.c_bool),
    ("print_realtime", ctypes.c_bool)
    ("print_timestampts", ctypes.c_bool),

    # [EXPERIMENTAL] token-level timestampts
    ("token_timestampts", ctypes.c_bool),
    ("thold_pt", ctypes.c_float),
    ("thold_ptsum", ctypes.c_float),
    ("max_len", ctypes.c_int),
    ("split_on_word", ctypes.c_bool),
    ("max_tokens", ctypes.c_int),

    # [EXPERIMENTAL]    
    ("debug_mode", ctypes.c_bool),
    ("audio_ctx", ctypes.c_int),

    # [EXPERIMENTAL]
    ("tdrz_enable", ctypes.c_bool),

    ("suppress_regex", ctypes.c_char_p),
    ("initial_prompt", ctypes.c_char_p),
    ("prompt_tokens", ctypes.POINTER(ctypes.c_int32)),
    ("prompt_n_tokens", ctypes.c_int),

    ("language", ctypes.c_char_p),
    ("detect_language", ctypes.c_bool),

    ("suppress_blank", ctypes.c_bool),
    ("suppress_nst", ctypes.c_bool),

    ("temperature", ctypes.c_float),
    ("max_initial_ts", ctypes.c_float),
    ("length_penalty", ctypes.c_float),

    ("temperature_inc", ctypes.c_float),
    ("entropy_thold", ctypes.c_float),
    ("logprob_thold", ctypes.c_float),
    ("no_speech_thold", ctypes.c_float),

    # TODO:  Finish
  ]

# Load library (singleton)

libwhisperpy: ctypes.CDLL | None = None,
libwhisperpy_ld_error: str | None = None
try:
  libwhisperpy = ctypes.CDLL(get_libwhisperpy_path())
except Exception as error:
  libwhisperpy_ld_error = f"Unable to load whisperpy backend library: {error}"
else:
  # Transcript context bindings
  libwhisperpy.transcript_context_make.argtypes = [ctypes.POINTER(TranscriptContext), ctypes.c_char_p]
  libwhisperpy.transcript_context_make.restype = ctypes.c_uint8

  libwhisperpy.transcript_context_free.argtypes = [ctypes.POINTER(TranscriptContext)]
  libwhisperpy.transcript_context_free.restype = ctypes.c_uint8

  libwhisperpy.speech_to_text.argtypes = [ctypes.c_char_p, ctypes.c_uint64, ctypes.POINTER(TranscriptContext), ctypes.c_char_p]
  libwhisperpy.speech_to_text.restype = ctypes.c_uint8

  # whisper.cpp bindings
  libwhisperpy.whisper_context_default_params.argtypes = []
  libwhisperpy.whisper_context_default_params.restype = WhisperContextParams

  libwhisperpy.whisper_full_default_params.argtypes = ctypes.c_int
  libwhisperpy.whisper_full_default_params.restype = WhisperFullParams
  

class WhisperpyLoader:
  """Allows to gain access to `libwhisperpy.so` `ctypes.CDLL` singleton instance.
  """
  def __init__(self):
    self._lib = libwhisperpy
    self._loading_error = libwhisperpy_ld_error
  
  def get(self):
    if self._loading_error is not None:
      raise RuntimeError(self._loading_error)
    return self._lib

  def __str__(self):
    return self._loading_error if self._loading_error is not None else ""

  def __bool__(self):
    return self._loading_error is None