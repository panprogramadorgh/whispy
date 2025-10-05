#include <vector>
#include <sstream>
#include <stdexcept>

#include <cstdint>
#include <cstdlib>
#include <cstring>

#include <whisper.h>

#include "whisperpy.h"
#include "utils.tpp"

/**
  struct whisper_context_params {
      bool  use_gpu;
      bool  flash_attn;
      int   gpu_device;  // cuda device

      // [experimental] token-level timestamps with dtw
      bool dtw_token_timestamps;
      enum whisper_alignment_heads_preset dtw_aheads_preset;

      int dtw_n_top;
      struct whisper_aheads dtw_aheads;

      size_t dtw_mem_size; // todo: remove
  };

  struct whisper_full_params {
      enum whisper_sampling_strategy strategy;

      int n_threads;
      int n_max_text_ctx;     // max tokens to use from past text as prompt for the decoder
      int offset_ms;          // start offset in ms
      int duration_ms;        // audio duration to process in ms

      bool translate;
      bool no_context;        // do not use past transcription (if any) as initial prompt for the decoder
      bool no_timestamps;     // do not generate timestamps
      bool single_segment;    // force single segment output (useful for streaming)
      bool print_special;     // print special tokens (e.g. <SOT>, <EOT>, <BEG>, etc.)
      bool print_progress;    // print progress information
      bool print_realtime;    // print results from within whisper.cpp (avoid it, use callback instead)
      bool print_timestamps;  // print timestamps for each text segment when printing realtime

      // [EXPERIMENTAL] token-level timestamps
      bool  token_timestamps; // enable token-level timestamps
      float thold_pt;         // timestamp token probability threshold (~0.01)
      float thold_ptsum;      // timestamp token sum probability threshold (~0.01)
      int   max_len;          // max segment length in characters
      bool  split_on_word;    // split on word rather than on token (when used with max_len)
      int   max_tokens;       // max tokens per segment (0 = no limit)

      // [EXPERIMENTAL] speed-up techniques
      // note: these can significantly reduce the quality of the output
      bool debug_mode;        // enable debug_mode provides extra info (eg. Dump log_mel)
      int  audio_ctx;         // overwrite the audio context size (0 = use default)

      // [EXPERIMENTAL] [TDRZ] tinydiarize
      bool tdrz_enable;       // enable tinydiarize speaker turn detection

      // A regular expression that matches tokens to suppress
      const char * suppress_regex;

      // tokens to provide to the whisper decoder as initial prompt
      // these are prepended to any existing text context from a previous call
      // use whisper_tokenize() to convert text to tokens
      // maximum of whisper_n_text_ctx()/2 tokens are used (typically 224)
      const char * initial_prompt;
      const whisper_token * prompt_tokens;
      int prompt_n_tokens;

      // for auto-detection, set to nullptr, "" or "auto"
      const char * language;
      bool detect_language;

      // common decoding parameters:
      bool suppress_blank; // ref: https://github.com/openai/whisper/blob/f82bc59f5ea234d4b97fb2860842ed38519f7e65/whisper/decoding.py#L89
      bool suppress_nst;   // non-speech tokens, ref: https://github.com/openai/whisper/blob/7858aa9c08d98f75575035ecd6481f462d66ca27/whisper/tokenizer.py#L224-L253

      float temperature;      // initial decoding temperature, ref: https://ai.stackexchange.com/a/32478
      float max_initial_ts;   // ref: https://github.com/openai/whisper/blob/f82bc59f5ea234d4b97fb2860842ed38519f7e65/whisper/decoding.py#L97
      float length_penalty;   // ref: https://github.com/openai/whisper/blob/f82bc59f5ea234d4b97fb2860842ed38519f7e65/whisper/transcribe.py#L267

      // fallback parameters
      // ref: https://github.com/openai/whisper/blob/f82bc59f5ea234d4b97fb2860842ed38519f7e65/whisper/transcribe.py#L274-L278
      float temperature_inc;
      float entropy_thold;    // similar to OpenAI's "compression_ratio_threshold"
      float logprob_thold;
      float no_speech_thold;

      struct {
          int best_of;    // ref: https://github.com/openai/whisper/blob/f82bc59f5ea234d4b97fb2860842ed38519f7e65/whisper/transcribe.py#L264
      } greedy;

      struct {
          int beam_size;  // ref: https://github.com/openai/whisper/blob/f82bc59f5ea234d4b97fb2860842ed38519f7e65/whisper/transcribe.py#L265

          float patience; // TODO: not implemented, ref: https://arxiv.org/pdf/2204.05424.pdf
      } beam_search;

      // called for every newly generated text segment
      whisper_new_segment_callback new_segment_callback;
      void * new_segment_callback_user_data;

      // called on each progress update
      whisper_progress_callback progress_callback;
      void * progress_callback_user_data;

      // called each time before the encoder starts
      whisper_encoder_begin_callback encoder_begin_callback;
      void * encoder_begin_callback_user_data;

      // called each time before ggml computation starts
      ggml_abort_callback abort_callback;
      void * abort_callback_user_data;

      // called by each decoder to filter obtained logits
      whisper_logits_filter_callback logits_filter_callback;
      void * logits_filter_callback_user_data;

      const whisper_grammar_element ** grammar_rules;
      size_t                           n_grammar_rules;
      size_t                           i_start_rule;
      float                            grammar_penalty;

      // Voice Activity Detection (VAD) params
      bool         vad;                         // Enable VAD
      const char * vad_model_path;              // Path to VAD model

      whisper_vad_params vad_params;
  };

*/

const std::uint8_t tc_error_message_length = 128;

extern "C"
{
  tcontext_state transcript_context_make(transcript_context *tc, const char *model_path)
  {
    std::vector<std::uint8_t> model_file;

    tc->last_error_code = TC_OK;

    try
    {
      tc->last_error_message = new char[tc_error_message_length];
    }
    catch (const std::exception &e)
    {
      tc->last_error_code = TC_MEMALLOC_ERROR;
      return TC_MEMALLOC_ERROR;
    }

    try
    {
      model_file = load_binary_data<std::uint8_t>(model_path);
    }
    catch (const std::exception &e)
    {
      std::string ferror_message = (std::ostringstream{} << "Could not load model file: " << e.what()).str();

      tc->last_error_code = TC_LOADMODEL_ERROR;
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
      tc->last_error_code = TC_INVWHISCTX_ERROR;
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

  tcontext_state speech_to_text(char *text, std::size_t text_size, transcript_context *tc, const char *speech_path)
  {
    std::vector<float> speech_file;
    std::size_t text_pos = 0;

    int wret = 0, nsegments = 0;
    const char *text_segment = nullptr;
    std::size_t writable_len = 0;

  if (tc->last_error_code != TC_OK)
    {
      return tc->last_error_code;
    }

    if (tc->model_context == nullptr)
    {
      tc->last_error_code = TC_INVWHISCTX_ERROR;
      std::strcpy(tc->last_error_message, "Model context is not initialied.");
      return TC_INVWHISCTX_ERROR;
    }

    try
    {
      speech_file = load_binary_data<float>(speech_path);
    }
    catch (const std::exception &e)
    {
      tc->last_error_code = TC_LOADSPEECH_ERROR;
      std::strcpy(tc->last_error_message, "Could not load speech audio file.");
      return TC_LOADSPEECH_ERROR;
    }

    whisper_full_params wparams = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
    wret = whisper_full(tc->model_context, wparams, speech_file.data(), speech_file.size());
    if (wret != 0)
    {
      tc->last_error_code = TC_SPEECHGEN_ERROR;
      std::strcpy(tc->last_error_message, "whisper_full failed.");
      return TC_SPEECHGEN_ERROR;
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