from typing import TypedDict, Literal
from os.path import join, dirname, exists
import ctypes

from .whisper_bindings import *
from .lib_loader import LibWhispy

# Paths

PACKAGE_ROOT = dirname(__file__)

def get_libwhispy_path():
  libs_path = join(PACKAGE_ROOT, "lib")
  libwhispy_path = join(libs_path, "libwhispy.so")
  if not exists(libwhispy_path):
    raise RuntimeError(f"Unable to find whispy backend library: {libwhispy_path}")
    
  return libwhispy_path


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

class whisper_context_params_dict(TypedDict, total=False):
  """whisper_context_params typed python dictionary.
  """

  use_gpu: bool | None
  flash_attn: bool | None
  gpu_device: int | None
  dtw_token_timestampts: bool | None
  dtw_aheads_preset: int | None
  dtw_n_top: int | None
  dtw_aheads: whisper_aheads | None # TODO: Typed fabric functions for nested structs.
  dtw_mem_size: int | None

def create_whisper_context_params(
  lib_loader: LibWhispy,
  partial_params: None | whisper_context_params_dict = None
) -> whisper_context_params:
  """Helps creating a `whisper_context_params` struct from a python dictionary.

  Args:
      lib_loader (LibWhispy): A healthy instance of the backend loaded.
      partial_params (None | whisper_context_params_dict, optional): Partial whisper context parameters provided by the user. Fields are optional and may even have None, is whose case it will be ignored. Defaults to None, which means to no modifications to the default configuration will be needed.

  Returns:
      whisper_context_params: A fulfilled struct with all the configurations whisper.cpp needs.
  """

  context_params = lib_loader.dll().whisper_context_default_params()

  if partial_params is None:
    return context_params

  for key, value in partial_params.items():
    if value is not None: setattr(context_params, key, value)
      
  return context_params


class whisper_full_params_dict(TypedDict, total=False):
  """whisper_full_params typed python dictionary.
  """

  strategy : int | None
  n_threads: int | None
  n_max_text_ctx: int | None
  offset_ms: int | None
  duration_ms: int | None
  translate: bool | None
  no_context: bool | None
  no_timestampts: bool | None
  single_segment: bool | None
  print_special: bool | None
  print_progress: bool | None
  print_realtime: bool | None
  print_timestampts: bool | None
  token_timestampts: bool | None
  thold_pt: float | None
  thold_ptsum: float | None
  max_len: int | None
  split_on_word: bool | None
  max_tokens: int | None
  debug_mode: bool | None
  audio_ctx: int | None
  tdrz_enable: bool | None
  suppress_regex: bytes | None
  initial_prompt: bytes | None
  prompt_tokens: ctypes.POINTER(ctypes.c_int32) | None # type: ignore
  prompt_n_tokens: int | None
  language: bytes | None
  detect_language: bool | None
  suppress_blank: bool  | None
  suppress_nst: bool | None
  temperature: float | None
  max_initial_ts: float | None
  length_penalty: float | None
  temperature_inc: float | None
  entropy_thold: float | None
  logprob_thold: float | None
  no_speech_thold: float | None
  new_segment_callback: whisper_new_segment_callback | None# type: ignore
  new_segment_callback_user_data: ctypes.c_void_p | None
  progress_callback: whisper_progress_callback | None # type: ignore
  profress_callback_user_data: ctypes.c_void_p | None
  encoder_begin_callback: whisper_encoder_begin_callback | None # type: ignore
  encoder_begin_callback_user_data: ctypes.c_void_p | None
  abort_callback: ggml_abort_callback | None # type: ignore
  abort_callback_user_data: ctypes.c_void_p | None
  logits_filter_callback: whisper_logits_filter_callback | None # type: ignore  
  logits_filter_callback_user_data: ctypes.c_void_p | None
  grammar_rules: ctypes.POINTER(ctypes.c_void_p) | None # type: ignore
  n_grammar_rules: int | None
  i_start_rule: int | None
  grammar_penalty: float | None


def create_whisper_full_params(
  lib_loader: LibWhispy,
  sampling: Literal["greedy"] | Literal["beam_search"],
  partial_params: None | whisper_full_params_dict = None
) -> whisper_full_params:
  """Helps creating a `whisper_full_params` struct from a python dictionary.

  Args:
      lib_loader (LibWhispy): A healthy instance of the backend loaded.
      partial_params (None | whisper_full_params_dict, optional): Partial whisper full parameters provided by the user. Fields are optional and may even have None, is whose case it will be ignored. Defaults to None, which means to no modifications to the default configuration will be needed.

  Returns:
      whisper_full_params: A fulfilled struct with all the configurations whisper.cpp needs.
  """

  wparams = lib_loader.dll().whisper_full_default_params(
    1 if sampling == "beam_search" else 0
  )
  if partial_params is None:
    return wparams
    
  for key, value in partial_params.items():   
    if value is not None: setattr(wparams, key, value)
  
  return wparams

    