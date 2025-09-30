#include <iostream>
#include <whisperpy.h>

int main()
{
  transcript_context ctx;
  char text[1024];

  transcript_context_make(&ctx, "./src/backend/whisper.cpp/models/ggml-base.bin");
  std::cout << "Transcript context was initialized" << '\n';

  speach_to_text(text, 1024, &ctx, "./inputs/jfk.pcmf32");

  transcript_context_free(&ctx);  
  std::cout << "Transcript context was freed" << '\n';

  std::cout << text << '\n';
}