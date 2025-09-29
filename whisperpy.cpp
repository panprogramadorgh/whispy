#include <iostream>
#include <fstream>
#include <iterator>
#include <vector>
#include <cstdint>
#include <stdexcept>
#include <type_traits>
#include <whisper.h>

enum tc_make_state
{
  TC_OK = 0,
  TC_LOADMODEL_ERROR = 1,
};

enum tc_speach_state
{
  TC_SPEACH_OK = 0,
  TC_INVWHISCTX_ERROR = 1,
  TC_LOADSPEACH_ERROR = 2
};

constexpr const std::uint8_t tc_error_message_length = 128;

struct transcript_context
{
  char *last_error_message[tc_error_message_length];
  whisper_context *model_context = nullptr;
};

template <typename T, std::enable_if_t<std::is_trivially_copyable_v<T>, int> = 0>
std::vector<T> load_binary_data(const std::string &file_path)
{
  // handle file
  std::ifstream file;
  std::streampos file_size;

  file.open(file_path, std::ios::binary);
  if (file.fail())
  {
    auto fpath = fs::path(file_path).string();
    auto context = std::ostringstream{} << "File stream is set to '" << file.rdstate() << '\'';
    throw std::runtime_error(context.str());
  }

  file.seekg(0, std::ios::end);
  file_size = file.tellg();
  if (file_size < 0)
  {
    auto fpath = fs::path(file_path).string();
    throw std::runtime_error("Failed to tellg() over file stream.");
  }
  file.seekg(0, std::ios::beg);

  // allocate and read
  if (static_cast<std::size_t>(file_size) % sizeof(T))
  {
    auto fpath = fs::path(file_path).string();
    throw std::runtime_error("Failed to reinterpret file contents.");
  }

  std::vector<T> t_buffer(static_cast<std::size_t>(file_size) / sizeof(T));
  file.read(reinterpret_cast<char *>(t_buffer.data()), static_cast<std::size_t>(file_size));

  // clean-up
  file.close();
  return t_buffer;
}

extern "C"
{
  tc_make_state make_transcript_context(transcript_context *tc, const char *model_path)
  {
    std::vector<std::uint8_t> model_file;
    try
    {
      model_file = load_binary_data<std::uint8_t>(model_path);
    }
    catch (const std::exception &e)
    {
      return TC_LOADMODEL_ERROR;
    }

    tc->model_context = whisper_init_from_buffer_with_params(
        model_file.data(),
        model_file.size(),
        whisper_context_default_params());

    if (tc->model_context == nullptr)
      return TC_LOADMODEL_ERROR;

    // clr errors
    for (std::size_t i = 0; i < tc_error_message_length; i++)
      tc->last_error_message[i] = '\0';

    return TC_OK;
  }

  tc_speach_state speach_to_text(char *text, std::size_t max_text_length, transcript_context *tc, const char *speach_path)
  {
    if (tc->model_context == nullptr)
      return TC_INVWHISCTX_ERROR;

    std::vector<float> speach_file;

    try
    {
      speach_file = load_binary_data<float>(speach_path);
    }
    catch (const std::exception &e)
    {
      return TC_LOADSPEACH_ERROR ;
    }

    whisper_full_params wparams = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
    whisper_full(odel_params);
  }
}