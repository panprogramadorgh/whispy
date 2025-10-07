import ctypes 
from .wrapper import WhisperpyLoader, TranscriptContext
from .utils import WhisperInitError, WhisperTextGenError, fetch_model_path, format_tc_error


class ModelParams:
  """Whisper model parameters.
  """
  def __init__(self):
    loader = WhisperpyLoader()
    if not loader:
      raise WhisperInitError(str(loader))
    self._libwhisperpy = loader.get()

    # TODO: Allow users to configure the return value of `whisper_context_default_params`

class SpeechParams:
  """Speech to text parameters.
  """
  def __init__(self):   
    loader = WhisperpyLoader()
    if not loader:
      raise WhisperInitError(str(loader))
    self._libwhisperpy = loader.get()

    # TODO: Allow users to configure `whisper_full` behaviour.


class WhisperModel:
  """
  A python wrapper class over the whisper.cpp library.
  """
  def __init__(self, model_name: str):
    """Simple clas

    Args:
        model_path: Anything used to construct a utf-8 bytes object.

    Raises:
        RuntimeError: If the underlying C api detects an error.
    """
    loader = WhisperpyLoader()
    if not loader:
      raise WhisperInitError(str(loader))
    self._libwhisperpy = loader.get()

    model_path = fetch_model_path(model_name)
    if model_path is None:
      raise WhisperInitError("No such model name")

    self._tc = TranscriptContext()
    make_result: int = self._libwhisperpy.transcript_context_make(ctypes.pointer(self._tc), model_path)
    if make_result != 0:
      raise WhisperInitError(fetch_model_path(self._tc))
  
  def speech_to_text(self, speech_path: str, max_text_size: int = (1 << 10) * 4):
    """Returns a string with the transcription of the speech.

    Args:
        speech_path: Anythin used to construct a utf-8 bytes object. 
    """
    text = (ctypes.c_char * max_text_size)()

    speech_result: int = self._libwhisperpy.speech_to_text(text, max_text_size, self._tc, bytes(speech_path, encoding="utf-8"))
    if speech_result != 0:
      raise WhisperTextGenError(format_tc_error(self._tc))

    encoded_text =  str(memoryview(text), encoding="utf-8")
    return encoded_text[:encoded_text.find('\0')]


def main():
  pass
if __name__ == "__main__":
  main()