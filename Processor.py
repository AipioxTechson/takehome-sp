from abc import ABC, abstractmethod

class Processor(ABC):
  '''Abstract class for a Processor'''

  @abstractmethod
  def process(self, listOfMessages: list[int]) -> None:
    pass
