import os
import sys
import unittest
import subprocess


class BasicTest(unittest.TestCase):

  def setUp(self):
    """Prepare a wheel for the package and temporary install the package in order to begin with the tests. 
    """
    pkgs_path = os.path.join(os.path.realpath("."), "src")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", os.path.join(pkgs_path, "requirements.txt")])
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkgs_path])

  def tearDown(self):
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "whispy"])

  def test_speech_to_text(self):
    # Import the package
    import whispy

    self.assertTrue(hasattr(whispy, "WhispyModel"), "whispery does not have 'WhispyModel' as an exported symbol.")
    self.assertTrue(hasattr(whispy, "WhisperInitError"), "whispery does not have 'WhisperInitError' as an exported symbol.")
    self.assertTrue(hasattr(whispy, "WhisperTextGenError"), "whispery does not have 'WhisperTextGenError' as an exported symbol.")

    # Init the model 
    from whispy import WhispyModel
    model = WhispyModel(model_name="base")
    print(model)
    
    # Transcribe
    output_text = model.speech_to_text("./inputs/jfk.pcmf33", sampling="greedy")
    target_output = "And so, my fellow Americans, ask not what your country can do for you, ask what you can do for your country."
    self.assertEqual(output_text, target_output)


if __name__ == "__main__":
  unittest.main()