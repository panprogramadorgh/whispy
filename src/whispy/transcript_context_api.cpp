#include <vector>
#include <sstream>
#include <stdexcept>

#include <cstdint>
#include <cstdlib>
#include <cstring>

#include <whisper.h>

#include "whispy.h"
#include "transcript_context_utils.tpp"

extern "C"
{
  /**
   * Initializes a `whispy_transcript_context` struct given the `model_path` and `cparams` provided.
   * 
   * @param tc A reference to a `whispy_transcript_context`.
   * @param model_path A character array containing the path to the model file.
   * @param cparams Internal transcript context's model initialization parameters. 
   * 
   * @returns The same state as the one within the transcript context.
   */
  whispy_tc_state whispy_tc_make(whispy_transcript_context *tc, const char *model_path, whisper_context_params cparams)
  {
    std::vector<std::uint8_t> model_file;

    // Initialize the context's internal state.
    try
    {
      tc->last_error_message = new char[tc_message_size];

      // Some implementations could work with libc under the hood.
      if (tc->last_error_message == nullptr)
        throw std::runtime_error("Memory allocation error");
    }
    catch (const std::exception &e)
    {
      return set_tc_state(*tc, whispy_tc_state::MEMALLOC_ERROR, e.what());
    }

    // Load the model file.
    try
    {
      model_file = load_binary_data<std::uint8_t>(model_path);
    }
    catch (const std::exception &e)
    {
      return set_tc_state(*tc, whispy_tc_state::LOADMODEL_ERROR, e.what());
    }

    tc->model_context = whisper_init_from_buffer_with_params(
        model_file.data(),
        model_file.size(),
        cparams);

    if (tc->model_context == nullptr)
      return set_tc_state(*tc, whispy_tc_state::INVWHISCTX_ERROR, "whisper_init_from_buffer_with_params() failed");

    return set_tc_state(*tc, whispy_tc_state::OK, nullptr);
  }

  /**
   * Frees the resources associated with a `whispy_transcript_context`.
   * 
   * @param tc Any `whispy_transcript_context`
   */
  void whispy_tc_free(whispy_transcript_context *tc)
  {
    if (tc == nullptr)
      return;
    tc->last_error_code = whispy_tc_state::FREEDCTX_ERROR;
    if (tc->last_error_message != nullptr)
      delete tc->last_error_message;
    if (tc->model_context != nullptr)
      whisper_free(tc->model_context);
  }

  /**
   * Generates plain text from an audio file.
   * 
   * @param text The destination where to place the resulting text.
   * @param text_size The text's memory block size. 
   * @param tc A healthy `whispy_transcript_context` that will be used to transcribe.
   * @param speech_path The path to the audio file that will be transcribed. The only supported audio format is raw pcm little endian 32-bits.
   */
  whispy_tc_state whispy_speech_to_text(char *text, std::size_t text_size, whispy_transcript_context *tc, const char *speech_path, whisper_full_params wparams)
  {
    std::vector<float> speech_file;
    std::size_t text_pos = 0;

    int wret = 0, nsegments = 0;
    const char *text_segment = nullptr;
    std::size_t writable_len = 0;

    if (tc->last_error_code != whispy_tc_state::OK)
      return tc->last_error_code;

    if (tc->model_context == nullptr)
      return set_tc_state(*tc, whispy_tc_state::INVWHISCTX_ERROR, "Bad whisper context");

    try
    {
      speech_file = load_binary_data<float>(speech_path);
    }
    catch (const std::exception &e)
    {
      return set_tc_state(*tc, whispy_tc_state::LOADSPEECH_ERROR, e.what());
    }

    wret = whisper_full(tc->model_context, wparams, speech_file.data(), speech_file.size());
    if (wret != 0)
    {
      return set_tc_state(*tc, whispy_tc_state::SPEECHGEN_ERROR, "whisper_full() failed");
    }

    nsegments = whisper_full_n_segments(tc->model_context);
    for (int i = 0; i < nsegments && text_pos < text_size - 1; i++)
    {
      text_segment = whisper_full_get_segment_text(tc->model_context, i);
      writable_len = std::min(std::strlen(text_segment), text_size - text_pos - 1);

      std::memcpy(
          text + text_pos,
          text_segment,
          writable_len);

      text_pos += writable_len;
    }
    text[text_pos] = '\0';

    return set_tc_state(*tc, whispy_tc_state::OK, nullptr); // Flushes any previous bad state.
  }
}