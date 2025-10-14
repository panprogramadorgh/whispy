import ctypes
from .utils import get_libwhispy_path
from .bindings import *

class LibWhispy:
  """Loads the backend library `libwhispy.so` using `ctypes.CDLL`.
  """
  def __init__(self):
    self._loading_error = ""
    try:
      self._lib_path = get_libwhispy_path()
      self._lib = ctypes.CDLL(self._lib_path)
    except Exception as e:
      self._loading_error = str(e)
    else:
      bind_c_api(self._lib)

  def dll(self):
    """Returns an instance of `ctypes.CDLL` with backend library loaded.

    Raises:
        RuntimeError: Throws in case there were an error loading the library and the consumer insists getting it.

    Returns:
        ctypes.CDLL: The backend shared library.
    """
    if len(self._loading_error):
      raise RuntimeError(self._loading_error)
    return self._lib
  
  @property 
  def lib_path(self):
    return self._lib_path
  
  @property 
  def loading_error(self):
    return self._loading_error

  def __bool__(self):
    return len(self._loading_error) == 0