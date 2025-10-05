from os.path import join, dirname
from wrapper import TranscriptContext 

PROJECT_ROOT = dirname(dirname(__file__))

# Errors

class WhisperInitError(RuntimeError):
  def __init__(self, detail: str | None):
    super().__init__(f"Model initialization error: {detail}")

class WhisperTextGenError(RuntimeError):
  def __init__(self, detail: str | None):
    super().__init__(f"Speech to text error: {detail}")


def format_tc_error(tc: TranscriptContext):
  """Provides format to messages related with backend errors.

  Args:
      tc (TranscriptContext): Backend resources.
      context (str | None, optional): Contextual string.

  Returns:
      str: A formatted string with the error message.
  """

  message = ""
  if tc.last_error_code != 0:
    message += str(tc.last_error_message, encoding="utf-8", errors="#")
  message += f" ({int(tc.last_error_code)})"
  return message


# Model selection 

MODELS = {
  "base": bytes(join(PROJECT_ROOT, "src", "backend", "whisper.cpp", "models", "ggml-base.bin"), encoding="utf-8")
}

def fetch_model_path(name: str):
  return MODELS.get(name)