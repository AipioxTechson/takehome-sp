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

class MockProcessor(Processor):
  '''Mock Processor used for Testing'''
  def __init__(self, expectedListOfMessages: list[list[int]]) -> None:
    self.expectedListOfMessages = expectedListOfMessages
    self.timesCalled = 0
    super().__init__()

  
  def process(self, listOfMessages: list[int]) -> None:
    '''Mocks implementation of Processor and checks for correct implementation'''

    assert self.timesCalled < len(self.expectedListOfMessages), "Process messages was called too many times"
    expectedList = self.expectedListOfMessages[self.timesCalled]
    self.timesCalled += 1

    assert expectedList == listOfMessages, "list of messages processed is not correct"