import os
import subprocess
import re
import shutil

# Package distribution
from setuptools import find_packages, Extension, setup
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion

REQUIRED_CMAKE_VERSION = "3.16"

def check_cmake_version(minimum_required: str):
  out = subprocess.check_output(["cmake", "--version"])
  coincidences = re.search(r"version\s*([\d.]+)", out.decode())
  if not len(coincidences.groups()): # It does not match
    return False

  cmake_version = coincidences.group(1)
  return LooseVersion(minimum_required) <= cmake_version


class CMakeExtension(Extension):
  def __init__(self, name: str):
    """CMake C++ module extension

    Args:
        name (str): The name of the module extension
    """

    super().__init__(name, sources=[])  

    self.sourcedir = os.path.dirname(os.path.dirname(__file__)) # Project root
    """Represents the root directory of the project
    """

class CMakeBuild(build_ext):
  """_summary_

  Args:
      build_ext (buld_ext): Used to build `CMakeExtension`s.
  """

  def run(self):
    if not check_cmake_version(REQUIRED_CMAKE_VERSION):
      raise RuntimeError(f"CMake >= '{REQUIRED_CMAKE_VERSION}' is needed.")

    for ext in self.extensions:
      self.build_extension(ext)

  def build_extension(self, ext: CMakeExtension):
    """Configures and builds the backend libraries.
    """

    print("Building", ext.name)

    cmake_build_dir =  os.path.join(ext.sourcedir, "cmake-debug-build" if self.debug else "cmake-build")
    """ CMake files
    """

    os.makedirs(cmake_build_dir, exist_ok=True)
    subprocess.check_call(["cmake", ext.sourcedir], cwd=cmake_build_dir)
    subprocess.check_call(["cmake", "--build", "."], cwd=cmake_build_dir)
    print()
  
  def move_libraries(self, ext: CMakeExtension):
    """Moves the C++ libraries inside the package.
    """

    cmake_build_dir =  os.path.join(ext.sourcedir, "cmake-debug-build" if self.debug else "cmake-build")
    """ CMake files
    """
    package_libraries_path = os.path.join(ext.sourcedir, "src", "whisperpy", "lib")
    """whisperpy C++ libraries
    """

    # TODO: Move libraries
    libraries = [
      "libwhisperpy.so",
      "src/backend/whisper.cpp/src/libwhisper.so*",
      "src/backend/whisper.cpp/src/ggml/src/libggml-base.so",
      "src/backend/whisper.cpp/src/ggml/src/libggml-cpu.so",
      "src/backend/whisper.cpp/src/ggml/src/libggml.so"
    ]

    shutil.copy(os.path.join(cmake_build_dir, "libwhisperpy.so"), os.path.join(package_libraries_path))
    shutil.copy(os.path.join(cmake_build_dir, "src/backend/whisper.cpp/src/libwhisper.so"), os.path.join(package_libraries_path))
    shutil.copy(os.path.join(cmake_build_dir, "src/backend/whisper.cpp/src/libwhisper.so"), os.path.join(package_libraries_path))

setup(
  name="whisperpy",
  version="1.1.1",
  author="panprogramador",
  author_email="",
  description="Speech to text transcriber.",
  long_description="",
  packages=find_packages("src"),
  package_dir={"": "src"},
  ext_modules=[CMakeExtension("whisperpy")],
  cmdclass=dict(build_ext=CMakeBuild)
)