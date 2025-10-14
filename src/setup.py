from typing import Sequence, Callable, Any
from os.path import join, dirname
from os import makedirs
import subprocess
import re
import shutil

from setuptools import find_packages, Extension, setup
from setuptools.command.build_ext import build_ext


# Constants

PROJECT_ROOT = dirname(dirname(__file__))


# CMake versions 

class LooseVersion:
  """Allows to compare two different semver format versions.
  """

  def __init__(self, sversion: str):
    self.version: tuple[str] = self.parse(sversion)

  def parse(self, obj: object):
    if not isinstance(obj, Sequence):
      raise RuntimeError("Iterable object is expected to be parsed.")
    ver_segments: tuple[str] = tuple(str(x) for x in obj if isinstance(x, str) and x and x != ".") # type: ignore
    return ver_segments


  def __eq__(self, other: object):
    other_parsed = self.parse(other)
    return self.version == other_parsed
  
  def __gt__(self, other: object) -> bool:
    other_parsed = self.parse(other)
    return self.version > other_parsed

  def __lt__(self, other: object) -> bool:
    other_parsed = self.parse(other)
    return self.version < other_parsed
  
  def __ge__(self, other: object) -> bool:
    other_parsed = self.parse(other)
    return self.version >= other_parsed

  def __le__(self, other: object) -> bool:
    other_parsed = self.parse(other)
    return self.version <= other_parsed

REQUIRED_CMAKE_VERSION = "3.16"

def check_cmake_version(minimum_required: str):
  out = subprocess.check_output(["cmake", "--version"])
  coincidences = re.search(r"version\s*([\d.]+)", out.decode())
  if coincidences is None or not len(coincidences.groups()): # It does not match
    return False

  cmake_version = coincidences.group(1)
  return LooseVersion(minimum_required) <= cmake_version


# CMake extensions

class CMakeExtension(Extension):
  def __init__(self, name: str, libraries: None | list[str] = None, on_finish: Callable[..., Any] | None = None):
    """CMake C++ module extension

    Args:
        name (str): The name of the module extension
    """

    super().__init__(name, sources=[], libraries=libraries)  

    self.sourcedir = PROJECT_ROOT
    """Represents the root directory of the project
    """

    self.on_finish = on_finish
    """A post compilation callback to be executed.
    """


class CMakeBuild(build_ext):
  """
  Args:
      build_ext (buld_ext): Used to build `CMakeExtension`s.
  """

  def run(self):
    if not check_cmake_version(REQUIRED_CMAKE_VERSION):
      raise RuntimeError(f"CMake >= '{REQUIRED_CMAKE_VERSION}' is needed.")

    for ext in self.extensions:
      self.build_extension(ext)
      print(f"Extension '{ext.name}' is done.")

      self.move_libraries(ext)
      print(f"Libraries for '{ext.name}' were moved.")

      ext.on_finish()
      print(f"'on_finish' callback is done.")



  def build_extension(self, ext: CMakeExtension):
    """Configures and builds the backend libraries.
    """

    print(f"Building extension '{ext.name}'")

    cmake_build_dir =  join(ext.sourcedir, "cmake-debug-build" if self.debug else "cmake-build")
    """ CMake files
    """

    makedirs(cmake_build_dir, exist_ok=True)
    subprocess.check_call(["cmake", ext.sourcedir], cwd=cmake_build_dir)
    subprocess.check_call(["cmake", "--build", "."], cwd=cmake_build_dir)
 

  def move_libraries(self, ext: CMakeExtension):
    """Moves the C++ libraries inside the package.
    """
    print(f"Moving '{ext.name}' libraries within the package.")

    cmake_build_dir =  join(ext.sourcedir, "cmake-debug-build" if self.debug else "cmake-build")
    """ CMake files
    """
    package_libraries_path = join(ext.sourcedir, "src", "whispy", "lib")
    """whispy C++ libraries
    """

    makedirs(package_libraries_path, exist_ok=True)

    for lib in ext.libraries:
      shutil.copy(join(cmake_build_dir, lib), package_libraries_path)
    

def download_ggml_model(model_name: str):
  origin = join(PROJECT_ROOT, "lib", "whisper.cpp", "models")
  subprocess.check_call([join(origin, "download-ggml-model.sh"), model_name])

  models_dir = join(PROJECT_ROOT, "src", "whispy", "models")
  makedirs(models_dir, exist_ok=True)
  shutil.copy(join(origin, f"ggml-{model_name}.bin"), models_dir)

setup(
  # Metadata
  name="whispy",
  version="2.0.0",
  author="panprogramador",
  author_email="",
  description="Speech to text transcriber.",
  long_description="",

  # Find the package
  packages=find_packages(where="."),
  package_dir={"": "."},

  # CMake extensions
  ext_modules=[
    CMakeExtension("whispy/libwhispy", [ 
        "libwhispy.so",

        "lib/whisper.cpp/src/libwhisper.so",    # symlink
        "lib/whisper.cpp/src/libwhisper.so.1",  # symlink
        "lib/whisper.cpp/src/libwhisper.so.1.7.4",

        "lib/whisper.cpp/ggml/src/libggml.so",
        "lib/whisper.cpp/ggml/src/libggml-base.so",
        "lib/whisper.cpp/ggml/src/libggml-cpu.so", 
      ],
      on_finish=lambda: download_ggml_model(model_name="base")
    )
  ],
  cmdclass=dict(build_ext=CMakeBuild),

  # Include the libraries and the model
  package_data= {
    "whispy": ["./lib/*", "./models/*"]
  }
)