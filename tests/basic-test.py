import sys
sys.path.append("src")
from whisperpy import WhisperModel

model = WhisperModel(model_name="base")
text = model.speach_to_text("./inputs/jfk.pcmf32")
print(text)