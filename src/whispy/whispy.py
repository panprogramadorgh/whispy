from typing import Literal, Callable
from functools import wraps
import ctypes 

from .whisper_bindings import *
from .utils import *


lib_loader = LibWhispy()

class ModelParams:
  """Instructs whispy how to initialize a model.

  # TODO: Validation system.
  """

  def __init__(
    self,
    model_name: Literal["base"], # Maybe TODO: Add more models
    use_gpu: bool | None = None,
    flash_attn: bool | None = None
  ):
    self._whispy_params = dict(
      model_name=model_name 
    )
    self._whisper_context_params_dict = whisper_context_params_dict(
        use_gpu=use_gpu,
        flash_attn=flash_attn
      )
  
  def _get_whispy_params(self):
    return self._whispy_params

  def _get_whisper_context_params(self):
    """Returns the underlying parameters.

    Returns:
        whisper_context_params: Parses the parameters to be passed to whisper.cpp.
    """

    cparams =  create_whisper_context_params(
      lib_loader,
      self._whisper_context_params_dict
    )
    return cparams
  
  def model_name(self, new_value: Literal["base"]):
    self._whispy_params["model_name"] = new_value
    return self

  def use_gpu(self, new_value: bool):
    self._whisper_context_params_dict["use_gpu"] = new_value
    return self
  
  def flash_attn(self, new_value: bool):
    self._whisper_context_params_dict["flash_attn"] = new_value
    return self
  

class SpeechToTextParams:
  """Instructs whispy how to transcribe.

  # TODO: Validation system.
  """

  def __init__(
    self,  
    sampling_strategy: Literal["greedy"] | Literal["beam_search"],
    n_threads: int | None = None,  
    translate: bool | None = None,
    no_timestampts: bool | None = None,
    print_special: bool | None = None,
    print_progress: bool | None = None,
    print_realtime: bool | None = None,
    print_timestampts: bool | None = None,
    token_timestampts: bool | None = None,
    language: bytes | None = None,
    detect_language: bool | None = None,
    temperature: float | None = None,
    new_segment_callback: Callable[[str], None] | None = None,
    progress_callback: Callable[[int], None] | None = None,
  ):
    @SpeechToTextParams._nscallback
    def nscallback(segment: str):
      if new_segment_callback is not None:
        new_segment_callback(segment)
    
    @SpeechToTextParams._prcallback
    def prcallback(progress: int):
      if progress_callback is not None:
        progress_callback(progress)

    self._whispy_params = dict(
      sampling_strategy=sampling_strategy 
    )

    self._wfull_params_dict = whisper_full_params_dict(
      n_threads=n_threads,
      translate=translate,
      no_timestampts=no_timestampts,
      print_special=print_special, 
      print_progress=print_progress,
      print_realtime=print_realtime,
      print_timestampts=print_timestampts,
      token_timestampts=token_timestampts,
      language=language,
      detect_language=detect_language,
      temperature=temperature,

      # Callbacks
      new_segment_callback=nscallback if new_segment_callback is not None else None,
      progress_callback=prcallback if progress_callback is not None else None
    )

  @classmethod
  def _nscallback(cls, func: Callable[[str], None]):
    """new_segment_callback decorator helper.
    
    The decorated function, that is indeed returned, needs to access `libwhispy.so` and it will be passed to the `whisper_full_params` struct.

    If for some reason, someone calls intentionally the callback and there were an error loading the library, it will raise a RuntimeError before even pass the parameters to `WhispyModel`.

    So we have to be careful and stick to the idea that the backend library is the only one in charge of executing the callback due to the previous reason.

    Backend library calls within `WhispyModel` are wrapped with meaningful exception messages.
    """
    @wraps(func)
    def wrapper(ctx: ctypes.c_void_p, state: ctypes.c_void_p, n_new: ctypes.c_int, user_data: ctypes.c_void_p):
      lib = lib_loader.dll()
      segments = b""

      n_segments: int = lib.whisper_full_n_segments(ctx).value
      seg_idx = n_segments - n_new.value
      while seg_idx < n_segments:
        segments += lib.whisper_full_get_segment_text(ctx, state, seg_idx)
        seg_idx += 1

      func(str(segments, encoding="utf-8"))

    return wrapper
  
  @classmethod
  def _prcallback(cls, func: Callable[[int], None]):
    @wraps(func)
    def wrapper(ctx: ctypes.c_void_p, state: ctypes.c_void_p, progress: ctypes.c_int, user_data: ctypes.c_void_p):
      func(progress.value)
    return wrapper

  def _get_whispy_parms(self):
    return self._whispy_params

  def _get_whisper_full_params(self):
    """Returns the underlying parameters.

    Returns:
        whisper_full_params: Parses the parameters to be passed to whisper.cpp.
    """
    wparams = create_whisper_full_params(
      lib_loader,
      self._whispy_params["sampling_strategy"], # type: ignore
      self._wfull_params_dict
    )
    return wparams

  def new_segment_callback(self, func: Callable[[str], None]):
    """Registers the new segment callback. New segment callbacks are called every time there is a new text segment.

    Args:
        func (Callable[[str], None]): A callback that receives text segments.

    Returns:
        SpeechToTextParams: A reference to the speech params object.
    """
    @SpeechToTextParams._nscallback
    def nscallback(segment: str):
      func(segment)
    self._wfull_params_dict["new_segment_callback"] = nscallback
    return self

  def progress_callback(self, func: Callable[[int], None]):
    @SpeechToTextParams._prcallback
    def nscallback(progress: int):
      func(progress)
    self._wfull_params_dict["progress_callback"] = nscallback
    return self


class WhispyModel:
  """
    # Whispy
    ## whisper.cpp binding for python

    Whispy is a lightweight python wrapper over whisper.cpp that allows to generate plain text from audio recordings.
  """
  def __init__(self, params: ModelParams = ModelParams("base")):
    """Simple clas

    Args:
        model_path: Anything used to construct a utf-8 bytes object.

    Raises:
        RuntimeError: If the underlying C api detects an error.
    """
    # Check if the library is loaded
    if not lib_loader:
      raise WhisperInitError(lib_loader.loading_error)
    self._libwhispy = lib_loader.dll()

    # Configure the tc
    model_path =\
      fetch_model_path(params._get_whispy_params()["model_name"])  # type: ignore
    if model_path is None:
      raise WhisperInitError("No such model name")
    
    self._tc = whispy_transcript_context()
    cparams = params._get_whisper_context_params() # type: ignore

    make_result: int = self._libwhispy.whispy_tc_make(
      ctypes.pointer(self._tc),
      model_path,
      cparams   
    )
    if make_result != 0:
      raise WhisperInitError(format_tc_error(self._tc))
  

  def speech_to_text(self, speech_path: str, params: SpeechToTextParams = SpeechToTextParams("greedy")):
    """Returns a string with the transcription of the speech.

    Args:
        speech_path: Ahything used to construct a utf-8 bytes object. 
    """
    MAX_TEXT_SIZE = (1 << 10) * 8 # 8 KiB: More than enough
    text = (ctypes.c_char * MAX_TEXT_SIZE)()

    wparams = params._get_whisper_full_params() # type: ignore
    speech_result: int =\
      self._libwhispy.whispy_speech_to_text(
        text,
        MAX_TEXT_SIZE,
        ctypes.pointer(self._tc),
        bytes(speech_path, encoding="utf-8"),
        wparams
      )

    if speech_result != 0:
      raise WhisperTextGenError(format_tc_error(self._tc))

    decoded_text = str(memoryview(text), encoding="utf-8")
    end_pos = decoded_text.find("\x00")
    return decoded_text[1: end_pos if end_pos > 0 else 0]
 

  def destroy(self):
    self._libwhispy.whispy_tc_free(ctypes.pointer(self._tc))


  def dll(self):
    """Advanced users utility. Highly recomended to see `wrapper.py` to know what's currently binded.

    Returns:
        ctypes.CDLL: Returns the underlying handle to `libwhispy.so`.
    """
    return self._libwhispy