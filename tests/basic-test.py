import unittest
from whisperpy import WhisperModel

class Basic(unittest.TestCase):
  def test_model_constructor(self):
      model = WhisperModel(model_name="base")
      print(model)
  
  def test_model_speech_to_text(self):
      model = WhisperModel(model_name="base")
      text = model.speech_to_text("./inputs/jfk.pcmf32")
      target = "And so, my fellow Americans, ask not what your country can do for you, ask what you can do for your country."
      self.assertEqual(text, target)

if __name__ == "__main__":
  unittest.main()