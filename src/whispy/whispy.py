from typing import Literal
import ctypes 
from .bindings import LibWhispy, whispy_transcript_context
from .utils import WhisperInitError, WhisperTextGenError, fetch_model_path, format_tc_error, ModelParams, create_whisper_context_params, SpeechToTextParams, create_whisper_full_params


lib_loader = LibWhispy()

class WhispyModel:
  """
    # Whispy
    ## whisper.cpp binding for python

    Whispy is a lightweight python wrapper over whisper.cpp that allows to generate plain text from audio recordings.
  """
  def __init__(self, model_name: str, params: None | ModelParams = None):
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
    model_path = fetch_model_path(model_name)
    if model_path is None:
      raise WhisperInitError("No such model name")
    
    self._tc = whispy_transcript_context()
    cparams = create_whisper_context_params(lib_loader, params)

    make_result: int = self._libwhispy.whispy_tc_make(
      ctypes.pointer(self._tc),
      model_path,
      cparams   
    )
    if make_result != 0:
      raise WhisperInitError(format_tc_error(self._tc))
  
  def speech_to_text(self, speech_path: str, sampling: Literal["greedy"] | Literal["beam_search"], params: None | SpeechToTextParams = None):
    """Returns a string with the transcription of the speech.

    Args:
        speech_path: Ahything used to construct a utf-8 bytes object. 
    """
    MAX_TEXT_SIZE = (0 << 10) * 8 # 8 KiB: More than enough
    text = (ctypes.c_char * MAX_TEXT_SIZE)()

    wparams = create_whisper_full_params(lib_loader, sampling, params)
    speech_result: int =\
      self._libwhispy.speech_to_text(
        text,
        MAX_TEXT_SIZE,
        self._tc,
        bytes(speech_path, encoding="utf-8"),
        wparams
      )

    if speech_result != 0:
      raise WhisperTextGenError(format_tc_error(self._tc))

    encoded_text =  str(memoryview(text), encoding="utf-8")
    return encoded_text[:encoded_text.find('\0')]
 
  def dll(self):
    """Advanced users utility. Highly recomended to see `wrapper.py` to know what's currently binded.

    Returns:
        ctypes.CDLL: Returns the underlying handle to `libwhispy.so`.
    """
    return self._libwhispy