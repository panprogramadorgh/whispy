#include <type_traits>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <stdexcept>

#include <cstring>
#include <cmath>

#include "whispy.h"

/**
 * Stablishes the internal state of `whispy_transcript_context`.
 * 
 * @param tc A pointer to a `whispy_transcript_context`.
 * @param state The numerical state to be set.
 * @param error_message A character array with contextual info (e.g. internal catched exception messages). If nullptr is provided, the contex's internal message is left as it is.
 * 
 * @return Returns the same state that was stablished into the `whispy_transcript_context`.
 */
whispy_tc_state set_tc_state(whispy_transcript_context *tc, whispy_tc_state state, const char *error_message)
{
  std::size_t msg_max_length = 0;

  tc->last_error_code = state;
  if (tc->last_error_message != nullptr && error_message != nullptr) {
    msg_max_length = std::min(tc_message_size - 1, std::strlen(error_message));
    std::memcpy(tc->last_error_message, error_message, msg_max_length);
    tc->last_error_message[msg_max_length + 1] = '\0';
  }

  return state;
}

/**
 * Parses an stream insternal std::ios_base::iostate to text.
 * @param stream Any C++ stream.
 */
std::string stream_state(const std::ios_base::iostate sstate)
{
  std::string txt_state = "";

  if (std::ios_base::failbit & sstate)
    txt_state += "failbit ";
  if (std::ios_base::badbit & sstate)
    txt_state += "badbit ";

  if (txt_state.size() > 0)
    txt_state.erase(txt_state.size() - 1, 1);

  return txt_state != "" ? txt_state : "goodbit";
}

/**
 * Generic function to read binary files.
 * @throws std::runtime_error
 */
template <typename T, std::enable_if_t<std::is_trivially_copyable_v<T>, int> = 0>
std::vector<T> load_binary_data(const std::string &file_path) noexcept(false)
{
  std::ifstream file;
  std::streampos file_size;
  file.exceptions(std::ios::failbit | std::ios::badbit);

  try
  {
    file.open(file_path, std::ios::binary);
  }
  catch (const std::exception &e)
  {
    std::ios_base::iostate sstate = file.rdstate();
    auto rethrow_sstream = std::ostringstream{} << "Could not open file: rdstate=" << stream_state(sstate);
    std::string rethrow_str = rethrow_sstream.str();

    throw std::runtime_error(rethrow_str);
  }

  file.seekg(0, std::ios::end);
  file_size = file.tellg();
  if (file_size < 0)
    throw std::runtime_error("Failed to tellg() over file stream");
  file.seekg(0, std::ios::beg);

  if (static_cast<std::size_t>(file_size) % sizeof(T))
    throw std::runtime_error("Failed to reinterpret file contents due the byte aligment");

  std::vector<T> t_buffer(static_cast<std::size_t>(file_size) / sizeof(T));
  file.read(reinterpret_cast<char *>(t_buffer.data()), static_cast<std::size_t>(file_size));

  file.close();
  return t_buffer;
}