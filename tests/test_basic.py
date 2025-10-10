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

    # Obtain the .whl filename
    # dist_path = os.path.join(pkgs_path, "dist")
    # whl_path: None | str = ""
    # for f_path in os.listdir(dist_path):
    #   if f_path.endswith(".whl"): whl_path = os.path.join(dist_path, f_path)

    # Generate the .whl file   
    # subprocess.check_call([sys.executable, "-m", "build", "-sw", pkgs_path]) 
    # self.assertIsNotNone(whl_path, "Failed to generate wheel file.")

    # Install the .whl as a package
    # subprocess.check_call([sys.executable, "-m", "pip", "install", whl_path])

  def tearDown(self):
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "whisperpy"])

  def test_speech_to_text(self):
    # Import the package
    import whisperpy

    self.assertTrue(hasattr(whisperpy, "WhisperModel"), "whispery does not have 'WhisperModel' as an exported symbol.")
    self.assertTrue(hasattr(whisperpy, "WhisperInitError"), "whispery does not have 'WhisperInitError' as an exported symbol.")
    self.assertTrue(hasattr(whisperpy, "WhisperTextGenError"), "whispery does not have 'WhisperTextGenError' as an exported symbol.")

    # Init the model 
    from whisperpy import WhisperModel
    model = WhisperModel(model_name="base")
    print(model)
    
    # Transcribe
    output_text = model.speech_to_text("./inputs/jfk.pcmf32")
    target_output = "And so, my fellow Americans, ask not what your country can do for you, ask what you can do for your country."
    self.assertEqual(output_text, target_output)


if __name__ == "__main__":
  unittest.main()