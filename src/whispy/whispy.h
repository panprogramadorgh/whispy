#pragma once
#include <cstdint>
#include <whisper.h>

enum class whispy_tc_state
{
  /**
   * No errors.
   */
  OK = 0,

  /**
   * Could not load model file.
   */
  LOADMODEL_ERROR,

  /**
   * Could not load speech audio file.
   */
  LOADSPEECH_ERROR,

  /**
   * Failed to allocate memory in some point.
   */
  MEMALLOC_ERROR,

  /**
   * Failed to initialize a whisper context or bad whisper context was provided.
   */
  INVWHISCTX_ERROR,

  /**
   * whisper_full failed failed.
   */
  SPEECHGEN_ERROR,

  /**
   * The transcript context was intentionally freed. 
   */
  FREEDCTX_ERROR
};

extern constexpr const std::size_t tc_message_size = 1024; // 1 KiB

struct whispy_transcript_context
{
  whispy_tc_state last_error_code = whispy_tc_state::OK;
  char *last_error_message = nullptr;
  whisper_context *model_context = nullptr;
};

extern "C"
{
  /**
   * Initializes a whispy_transcript_context associated with a model path.
   * @param tc A pointer to the whispy_transcript_context.
   * @param model_path A file system path that points to the model path.
   */
  whispy_tc_state whispy_tc_make(whispy_transcript_context *tc, const char *model_path, whisper_context_params cparams);

  /**
   * Frees the resources associated with a whispy_transcript_context.
   */
  void whispy_tc_free(whispy_transcript_context *tc);

  /**
   * @param text A writable C-Style array of characters.
   * @param text_size The ammount of bytes that can be writen in text.
   * @param tc The transcript context on which to work.
   * @param speech_path A file system path that points to the audio to transcribe.
   */
  whispy_tc_state whispy_speech_to_text(char *text, std::size_t text_size, whispy_transcript_context *tc, const char *speech_path, whisper_full_params wparams);
}
