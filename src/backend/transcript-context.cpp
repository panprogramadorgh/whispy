#include <vector>
#include <sstream>
#include <stdexcept>

#include <cstdint>
#include <cstdlib>
#include <cstring>

#include <whisper.h>

#include "whisperpy.h"
#include "utils.tpp"

const std::uint8_t tc_error_message_length = 128;

extern "C"
{
  tcontext_state transcript_context_make(transcript_context *tc, const char *model_path)
  {
    std::vector<std::uint8_t> model_file;

    tc->last_error = TC_OK;

    try
    {
      tc->last_error_message = new char[tc_error_message_length];
    }
    catch (const std::exception &e)
    {
      tc->last_error = TC_MEMALLOC_ERROR;
      return TC_MEMALLOC_ERROR;
    }

    try
    {
      model_file = load_binary_data<std::uint8_t>(model_path);
    }
    catch (const std::exception &e)
    {
      std::string ferror_message = (std::ostringstream{} << "Could not load model file: " << e.what()).str();

      tc->last_error = TC_LOADMODEL_ERROR;
      std::memcpy(
          tc->last_error_message,
          ferror_message.c_str(),
          std::min(ferror_message.size(), static_cast<std::size_t>(tc_error_message_length)));
      return TC_LOADMODEL_ERROR;
    }

    tc->model_context = whisper_init_from_buffer_with_params(
        model_file.data(),
        model_file.size(),
        whisper_context_default_params());

    if (tc->model_context == nullptr)
    {
      tc->last_error = TC_INVWHISCTX_ERROR;
      std::strcpy(
          tc->last_error_message,
          "Could not initialize whisper context.");
      return TC_INVWHISCTX_ERROR;
    }

    return TC_OK;
  }

  void transcript_context_free(transcript_context *tc)
  {
    if (tc == nullptr)
      return;
    if (tc->last_error_message != nullptr)
      delete tc->last_error_message;
    if (tc->model_context != nullptr)
      whisper_free(tc->model_context);
  }

  tcontext_state speach_to_text(char *text, std::size_t text_size, transcript_context *tc, const char *speach_path)
  {
    std::vector<float> speach_file;
    std::size_t text_pos = 0;

    int wret = 0, nsegments = 0;
    const char *text_segment = nullptr;
    std::size_t writable_len = 0;

    if (tc->last_error != TC_OK)
    {
      return tc->last_error;
    }

    if (tc->model_context == nullptr)
    {
      tc->last_error = TC_INVWHISCTX_ERROR;
      std::strcpy(tc->last_error_message, "Model context is not initialied.");
      return TC_INVWHISCTX_ERROR;
    }

    try
    {
      speach_file = load_binary_data<float>(speach_path);
    }
    catch (const std::exception &e)
    {
      tc->last_error = TC_LOADSPEACH_ERROR;
      std::strcpy(tc->last_error_message, "Could not load speach audio file.");
      return TC_LOADSPEACH_ERROR;
    }

    whisper_full_params wparams = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
    wret = whisper_full(tc->model_context, wparams, speach_file.data(), speach_file.size());
    if (wret != 0)
    {
      tc->last_error = TC_SPEACHGEN_ERROR;
      std::strcpy(tc->last_error_message, "whisper_full failed.");
      return TC_SPEACHGEN_ERROR;
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

    return TC_OK;
  }
}