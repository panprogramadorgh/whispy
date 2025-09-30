import sys
sys.path.append("src")
from whisperpy import WhisperModel

speach_file = input("Enter an audio file to transcribe: ").strip()

model_config = {
  "model_name": "base"
}
model: WhisperModel | None = None

try:
  model = WhisperModel(**model_config)
except Exception as error:
  sys.stderr.write(str(error) + '\n')
  sys.exit(1)

text: str | None = None
try:
  text = model.speach_to_text(speach_file, max_text_size=256)
except Exception as error:
  sys.stderr.write(str(error) + '\n')
  sys.exit(1)

print("Transcript result:\n" + text)
