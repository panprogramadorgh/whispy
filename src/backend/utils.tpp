#include <type_traits>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <stdexcept>

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