#include <iostream>

extern "C"
{
#include <libavformat/avformat.h>
}

int main()
{
  AVFormatContext *ctx = nullptr;

  if (avformat_open_input(&ctx, "/home/alvaro/.trash/test_recordings/test.mp3", nullptr, nullptr))
  {
    throw std::runtime_error("avformat_open_input failed");
  }

  std::cout << "Hello World !" << '\n';

  return 0;
}
