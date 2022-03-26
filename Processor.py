from abc import ABC, abstractmethod

class Processor(ABC):
  '''Abstract class for a Processor'''

  @abstractmethod
  def process(self, listOfMessages: list[int]) -> None:
    pass


class DriverProcessor(Processor):
  '''Driver code for the Processor'''

  def process(self, listOfMessages: list[int]) -> None:
      print(listOfMessages)
