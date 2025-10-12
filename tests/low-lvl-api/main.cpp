#include <iostream>
#include <cstdlib>
#include <whispy.h>

int main()
{
  whispy_transcript_context ctx;
  char text[1024];

  whispy_tc_make(&ctx, "./src/backend/whisper.cpp/models/ggml-base.bin", whisper_context_default_params());
  std::cout << "Transcript context was initialized" << '\n';

  whispy_tc_state ret = whispy_speech_to_text(text, 1024, &ctx, "./inputs/jfk.pcmf32", whisper_full_default_params(WHISPER_SAMPLING_GREEDY));
  if (ret != whispy_tc_state::OK)
  {
    std::cerr << ctx.last_error_message << ": " << static_cast<int>(ctx.last_error_code ) << '\n';
    std::exit(1);
  }

  whispy_tc_free(&ctx);  
  std::cout << "Transcript context was freed" << '\n';

  std::cout << text << '\n';
}