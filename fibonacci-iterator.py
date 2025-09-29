from typing import Iterable

class FibonacciSequence:
  def __init__(self, begin: int, end: int):
    self.pos =  begin
    self.end = end

  def __iter__(self):
    return self

  def __next__(self):
    if self.pos == -1 or self.pos < self.end:
      prev = self.pos
      self.pos += 1
      return FibonacciSequence._fibonacci(prev)
    else:
      raise StopIteration

  def __contains__(self, item: int):
    if not isinstance(item, int):
      return False 
    if item < 0:
      return False
    cpos = self.pos
    while True:
      n = FibonacciSequence._fibonacci(cpos)
      if cpos > -1 and cpos >= self.end:
        break
      else:
        cpos += 1
      if n == item:
        return True
    return False

    
  @classmethod 
  def _fibonacci(cls, n: int):
    a, b, c = (1, 2, 0)
    if n <= 2:
      return n
    n -= 1
    while n > 0:
      c = b
      b += a
      a = c
      n -= 1
    return a


def print_numerical_sequence(seq: Iterable):
  for e in seq:
    print(e)

fib = FibonacciSequence(0, 10)
print_numerical_sequence(fib)
