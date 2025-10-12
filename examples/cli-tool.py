import sys
sys.path.append("src")
import whispy
from whispy import WhispyModel

# Input file
speech_file = input("Enter an audio file to transcribe: ").strip()
if not speech_file:
  print("Taking default input file.")
  speech_file = "./inputs/jfk.pcmf32"

# Init model
model: WhispyModel
try:
  model = WhispyModel(model_name="base", params={"use_gpu": False})
except whispy.WhisperInitError as error:
  sys.stderr.write(str(error) + '\n')
  sys.exit(1)

# Transcribe
text = ""
try:
  text = model.speech_to_text(speech_file, presset="greedy", params={"n_threads": 4})
except whispy.WhisperTextGenError as error:
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