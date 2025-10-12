from typing import TypedDict, Literal
from os.path import join, dirname
import ctypes
from .bindings import\
  whispy_transcript_context,\
  whisper_aheads,\
  whisper_context_params,\
  whisper_full_params,\
  whisper_new_segment_callback,\
  whisper_progress_callback,\
  whisper_encoder_begin_callback,\
  ggml_abort_callback,\
  whisper_logits_filter_callback,\
  LibWhispy

# Constants

PACKAGE_ROOT = dirname(dirname(__file__))


# Data type parsing

int8 = int
int16 = int
int32 = int
int64 = int

uint8 = int
uint16 = int
uint32 = int
uint64 = int

double = float

PYTYPE_TO_CTYPE_PARSE_MAP: dict[type, type] = {
  bool: ctypes.c_bool,

  int8: ctypes.c_int8,
  int16: ctypes.c_int16,
  int32: ctypes.c_int32,
  int64: ctypes.c_int64,

  uint8: ctypes.c_uint8,
  uint16: ctypes.c_uint16,
  uint32: ctypes.c_uint32,
  uint64: ctypes.c_uint64,

  float: ctypes.c_float,
  double: ctypes.c_double
}

def is_ctypes_class(cls: object):
  return isinstance(cls, type) and isinstance(cls, ctypes._SimpleCData) # type: ignore


# Model selection 

MODELS = {
  "base": bytes(join(PACKAGE_ROOT, "models", "ggml-base.bin"), encoding="utf-8")
}

def fetch_model_path(name: str):
  return MODELS.get(name)


# Errors

class WhisperInitError(RuntimeError):
  def __init__(self, detail: str | None):
    super().__init__(f"Model initialization error: {detail}")

class WhisperTextGenError(RuntimeError):
  def __init__(self, detail: str | None):
    super().__init__(f"Speech to text error: {detail}")


def format_tc_error(tc: whispy_transcript_context):
  """Provides format to messages related with backend errors.

  Args:
      tc (TranscriptContext): Backend resources.
      context (str | None, optional): Contextual string.

  Returns:
      str: A formatted string with the error message.
  """   

  message = ""
  if tc.last_error_code != 0:
    message += str(tc.last_error_message, encoding="utf-8")
  message += f" (whispy_tc_state={int(tc.last_error_code)})"
  return message



# Model params

class ModelParams(TypedDict, total=False):
  """Whispy model configuration parameters.
  """

  use_gpu: bool
  flash_attn: bool
  gpu_device: int
  dtw_token_timestampts: bool
  dtw_aheads_preset: int
  dtw_n_top: int
  dtw_aheads: whisper_aheads # TODO: Typed fabric
  dtw_mem_size: int

def create_whisper_context_params(lib_loader: LibWhispy, partial_params: None | ModelParams = None) -> whisper_context_params:
  context_params = lib_loader.dll().whisper_context_default_params()

  if partial_params is None:
    return context_params

  for key, value in partial_params.items():
    param_type = ModelParams.__annotations__[key]
    param_ctype = PYTYPE_TO_CTYPE_PARSE_MAP.get(param_type)

    if param_ctype is None and\
      not is_ctypes_class(param_type):
      raise TypeError(f"Unsupported data type for '{key}' key: {param_type}")

    context_params[key] = param_ctype(value) if param_ctype is not None else value
      
  return context_params


class SpeechToTextParams(TypedDict, total=False):
  strategy: int
  n_threads: int
  n_max_text_ctx: int
  offset_ms: int
  duration_ms: int
  translate: bool
  no_context: bool
  no_timestampts: bool
  single_segment: bool
  print_special: bool
  print_progress: bool
  print_realtime: bool
  print_timestampts: bool
  token_timestampts: bool
  thold_pt: float
  thold_ptsum: float
  max_len: int
  split_on_word: bool
  max_tokens: int
  debug_mode: bool
  audio_ctx: int
  tdrz_enable: bool
  suppress_regex: bytes
  initial_prompt: bytes
  prompt_tokens: ctypes.POINTER(ctypes.c_int32) # type: ignore
  prompt_n_tokens: int 
  language: bytes
  detect_language: bool
  suppress_blank: bool 
  suppress_nst: bool
  temperature: float
  max_initial_ts: float
  length_penalty: float
  temperature_inc: float
  entropy_thold: float
  logprob_thold: float
  no_speech_thold: float
  new_segment_callback: whisper_new_segment_callback # type: ignore
  new_segment_callback_user_data: ctypes.c_void_p
  progress_callback: whisper_progress_callback # type: ignore
  profress_callback_user_data: ctypes.c_voidp
  encoder_begin_callback: whisper_encoder_begin_callback # type: ignore
  encoder_begin_callback_user_data: ctypes.c_void_p
  abort_callback: ggml_abort_callback # type: ignore
  abort_callback_user_data: ctypes.c_void_p
  logits_filter_callback: whisper_logits_filter_callback # type: ignore  
  logits_filter_callback_user_data: ctypes.c_void_p
  grammar_rules: ctypes.POINTER(ctypes.c_void_p) # type: ignore
  n_grammar_rules: int
  i_start_rule: int
  grammar_penalty: float


def create_whisper_full_params(lib_loader: LibWhispy, sampling: Literal["greedy"] | Literal["beam_search"], partial_params: None | SpeechToTextParams = None) -> whisper_full_params:
  wparams = lib_loader.dll().whisper_full_default_params(
    1 if sampling == "beam_search" else 0
  )
  if partial_params is None:
    return wparams
    
  for key, value in partial_params.items():   
    param_type = SpeechToTextParams.__annotations__[key]
    param_ctype = PYTYPE_TO_CTYPE_PARSE_MAP.get(param_type)

    if param_ctype is None and\
      not is_ctypes_class(param_type):
      raise TypeError(f"Unsupported data type for '{key}' key: {param_type}")

    wparams[key] = param_ctype(value) if param_ctype is not None else value
  
  return wparams

    