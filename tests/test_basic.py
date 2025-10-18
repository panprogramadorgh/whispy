import os
import sys
import unittest
import subprocess


class BasicTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    """Prepare a wheel for the package and temporary install the package in order to begin with the tests. 
    """
    pkgs_path = os.path.join(os.path.realpath("."), "src")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", os.path.join(pkgs_path, "requirements.txt")])
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkgs_path])

  @classmethod
  def tearDownClass(cls):
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "whispy"])

  def test_speech_to_text(self):
    # Import the package
    import whispy

    self.assertTrue(hasattr(whispy, "WhispyModel"), "whispery does not have 'WhispyModel' as an exported symbol.")
    self.assertTrue(hasattr(whispy, "ModelParams"), "whispery does not have 'ModelParams' as an exported symbol.")
    self.assertTrue(hasattr(whispy, "SpeechToTextParams"), "whispery does not have 'SpeechToTextParams' as an exported symbol.")
    self.assertTrue(hasattr(whispy, "WhisperInitError"), "whispery does not have 'WhisperInitError' as an exported symbol.")
    self.assertTrue(hasattr(whispy, "WhisperTextGenError"), "whispery does not have 'WhisperTextGenError' as an exported symbol.")
    print("Whispy was loaded:", whispy)

    # Init the model 
    model = whispy.WhispyModel(whispy.ModelParams(model_name="base", use_gpu=False, flash_attn=True))
    print("Model was loaded:", model)
    
    # Transcribe
    wfull_params = whispy.SpeechToTextParams("greedy")

    @wfull_params.progress_callback
    def print_progress(progress: int): # type: ignore
      print(f"- {progress}")

    output_text = model.speech_to_text("./inputs/jfk.pcmf32", wfull_params)
    print("The resulting text is:", output_text)
    self.assertTrue(output_text.lower().count("my fellow americans") > 0)
    self.assertTrue(output_text.lower().count("ask not what your country can do for you") > 0)
    self.assertTrue(output_text.lower().count("ask what you can do for your country") > 0)

    model.destroy()
    print("Model was destroyed.")


if __name__ == "__main__":
  unittest.main()