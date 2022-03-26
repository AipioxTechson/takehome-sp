from abc import ABC, abstractmethod

class Processor(ABC):
  '''Abstract class for a Processor'''

  @abstractmethod
  def process(self, list_of_messages: list[int]) -> None:
    pass


class DriverProcessor(Processor):
  '''Driver code for the Processor'''

  def process(self, list_of_messages: list[int]) -> None:
      print(list_of_messages)

class MockProcessor(Processor):
  '''Mock Processor used for Testing'''
  def __init__(self, expected_list_of_messages: list[list[int]]) -> None:
    self.expected_list_of_messages = expected_list_of_messages
    self.times_called = 0
    super().__init__()

  
  def process(self, list_of_messages: list[int]) -> None:
    '''Mocks implementation of Processor and checks for correct implementation'''

    assert self.times_called < len(self.expected_list_of_messages), "Process messages was called too many times"
    expected_list = self.expected_list_of_messages[self.times_called]
    self.times_called += 1

    assert expected_list == list_of_messages, "list of messages processed is not correct"