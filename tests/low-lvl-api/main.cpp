#include <iostream>
#include <cstdlib>
#include <whisperpy.h>

int main()
{
  transcript_context ctx;
  char text[1024];

  transcript_context_make(&ctx, "./src/backend/whisper.cpp/models/ggml-base.bin");
  std::cout << "Transcript context was initialized" << '\n';

  tcontext_state ret = speech_to_text(text, 1024, &ctx, "./inputs/jfk.pcmf32");
  if (ret != TC_OK)
  {
    std::cerr << ctx.last_error_message << ": " << ctx.last_error_code << '\n';
    std::exit(1);
  }

  transcript_context_free(&ctx);  
  std::cout << "Transcript context was freed" << '\n';

  std::cout << text << '\n';
}