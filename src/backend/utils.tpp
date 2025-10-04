#include <type_traits>
#include <vector>
#include <string>
#include <fstream>
#include <stdexcept>

/**
 * Generic function to read binary files.
 * @throws std::runtime_error
 */
template <typename T, std::enable_if_t<std::is_trivially_copyable_v<T>, int> = 0>
std::vector<T> load_binary_data(const std::string &file_path) noexcept(false)
{
  std::ifstream file;
  std::streampos file_size;

  file.open(file_path, std::ios::binary);
  if (file.fail())
    throw std::runtime_error("Could not open file");

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