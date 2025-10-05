#include <cstdint>
#include <whisper.h>

extern "C"
{
  enum tcontext_state
  {
    /**
     * No errors.
     */
    TC_OK = 0,

    /**
     * Could not load model file.
     */
    TC_LOADMODEL_ERROR,

    /**
     * Could not load speech audio file.
     */
    TC_LOADSPEECH_ERROR,

    /**
     * Failed to allocate memory in some point.
     */
    TC_MEMALLOC_ERROR,

    /**
     * Failed to initialize the whisper context or bad whisper context were provided.
     */
    TC_INVWHISCTX_ERROR,

    /**
     * whisper_full failed to generate segments.
     */
    TC_SPEECHGEN_ERROR
  };

  extern constexpr const std::size_t tc_error_message_length = 512;

  struct transcript_context
  {
    tcontext_state last_error_code = TC_OK;
    char *last_error_message = nullptr;
    whisper_context *model_context = nullptr;
  };

  /**
   * Initializes a transcript_context associated with a model path.
   * @param tc A pointer to the transcript_context.
   * @param model_path A file system path that points to the model path.
   */
  tcontext_state transcript_context_make(transcript_context *tc, const char *model_path);

  /**
   * Frees the resources associated with a transcript_context.
   */
  void transcript_context_free(transcript_context *tc);

  /**
   * @param text A writable C-Style array of characters.
   * @param text_size The ammount of bytes that can be writen in text.
   * @param tc The transcript context on which to work.
   * @param speech_path A file system path that points to the audio to transcribe.
   */
  tcontext_state speech_to_text(char *text, std::size_t text_size, transcript_context *tc, const char *speech_path);
}
