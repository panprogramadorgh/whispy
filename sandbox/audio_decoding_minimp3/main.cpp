#define MINIMP3_IMPLEMENTATION
#undef MINIMP3_NO_STDIO

#include <iostream>
#include <sstream>
#include <string> 
#include <filesystem> 
#include <stdexcept>
#include <cstdint>

#include <minimp3_ex.h>

namespace fs = std::filesystem;

/**
 * Decodes MP3 audio files into int16 PCM.
 * Then reinterpretates the buffer to be std::uint8_t.
 */
int main() {
  std::string file_path = "";
  mp3dec_t decoding_context;
  mp3dec_file_info_t decoded_info;

  std::cout << "Enter an audio file path (*.mp3): ";
  std::cin >> file_path;
  if (!fs::exists(file_path)) throw std::runtime_error("No such file.");

  int ret = mp3dec_load(&decoding_context, file_path.c_str(), &decoded_info, nullptr, nullptr);
  if (ret || decoded_info.samples == 0) {
    throw std::runtime_error((std::ostringstream{} << "Audio decoding error: " << ret).str());
  }

  // Int16 little endian
  // for (std::size_t i = 0; i < decoded_info.samples; i++) {
  //   std::cout << decoded_info.buffer[i] << ";  ";
  // }

  auto audio_bytes = reinterpret_cast<std::uint8_t *>(decoded_info.buffer);
  std::size_t audio_bytes_len = decoded_info.samples * sizeof(mp3d_sample_t);

  for (std::size_t i = 0; i < audio_bytes_len; i++) {
    std::cout << static_cast<int>(audio_bytes[i]) << ",  ";
  }
}