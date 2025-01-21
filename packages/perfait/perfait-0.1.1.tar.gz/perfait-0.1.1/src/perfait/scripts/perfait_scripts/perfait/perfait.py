import time

class Stopwatch:
  @classmethod
  def get_time(cls):
    return time.perf_counter()

  def __init__(self):
    self.reset()

  def reset(self):
    self.__StartTime = Stopwatch.get_time()

  def elapsed_time(self):
    return Stopwatch.get_time() - self.__StartTime
