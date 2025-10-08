import os
import sys
import unittest
import subprocess


class BasicTest(unittest.TestCase):
  """TODO: Prepare wheel
  """

  def setUp(self):
    """Prepare a wheel for the package and temporary install the package in order to begin with the tests. 
    """

    subprocess.check_call([sys.executable, "-m", "build", "-sw"])    
    subprocess.check_call([sys.executable, "-m", "pip", "install", ])

  def test_import(self):
    """Test to import the package
    """

    import whisperpy
    self.assertTrue(hasattr(whisperpy, "WhisperModel"), "whispery does not have 'WhisperModel' as an exported symbol.")
    self.assertTrue(hasattr(whisperpy, "WhisperInitError"), "whispery does not have 'WhisperInitError' as an exported symbol.")
    self.assertTrue(hasattr(whisperpy, "WhisperTextGenError"), "whispery does not have 'WhisperTextGenError' as an exported symbol.")

  def test_model_constructor(self):
      from whisperpy import WhisperModel
      model = WhisperModel(model_name="base")
      print(model)
  
  def test_model_speech_to_text(self):
      from whisperpy import WhisperModel
      model = WhisperModel(model_name="base")
      output_text = model.speech_to_text("./inputs/jfk.pcmf32")
      target_output = "And so, my fellow Americans, ask not what your country can do for you, ask what you can do for your country."
      self.assertEqual(output_text, target_output)


if __name__ == "__main__":
  unittest.main()