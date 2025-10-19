#include <iostream>

extern "C"
{
#include <libavformat/avformat.h>
}

/**
 * A simple program that detects an audio file's format.
 */
int main()
{
  AVFormatContext *ctx = nullptr;
  const char input_file[] = "/home/alvaro/.trash/test_recordings/test.mp3";

  // Check what's the input audio file's format.
  if (avformat_open_input(&ctx, input_file, nullptr, nullptr))
  {
    throw std::runtime_error("avformat_open_input failed");
  }
  const char *fname = ctx->iformat->name;

  // clean-up
  avformat_close_input(&ctx);

  std::cout << input_file << '\t' << fname << '\n';
  return 0;
}
