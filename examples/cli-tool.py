import sys
sys.path.append("src")
import whisperpy
from whisperpy import WhisperModel

# Input file
speach_file = input("Enter an audio file to transcribe:").strip()
if not speach_file:
  print("Taking default input file.")
  speach_file = "./inputs/jfk.pcmf32"

# Init model
model_config = {
  "model_name": "base"
}
model: WhisperModel | None = None

try:
  model = WhisperModel(**model_config)
except whisperpy.WhisperInitError as error:
  sys.stderr.write(str(error) + '\n')
  sys.exit(1)

# Transcribe
text: str | None = None
try:
  text = model.speach_to_text(speach_file, max_text_size=4096).strip()
except whisperpy.WhisperTextGenError as error:
  sys.stderr.write(str(error) + '\n')
  sys.exit(1)

print("Transcript result:\n" + text)

# Save the file
saveFile = input("Write output to disk [Y/N] ? ").strip().lower() == "y"
if not saveFile:
  sys.exit(0)

outputPath = input("Enter the output file path: ").strip()
with open(outputPath, "w") as outputFile:
  outputFile.write(text)
print("Done !")