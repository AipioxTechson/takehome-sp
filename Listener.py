from abc import ABC, abstractmethod
from threading import Lock

from Processor import DriverProcessor, Processor


class Listener(ABC):
  '''Abstract model for a Collating Listener'''

  def __init__(self, processor: Processor) -> None:
    self.processor = processor
    super().__init__()

  abstractmethod
  async def process(self, messages: list[int]) -> None:
    '''Recieves a list of messages and invokes the processor when a stream of messages comes in'''
    pass


class collatingListener(Listener):
  '''
  This class represents the implementation for a Listener
  '''
  def __init__(self, processor: Processor, messagesObtained: set[int], messageLock: Lock):
    super().__init__(processor)
    self.curKey = 0
    self.messagesObtained = messagesObtained
    self.lock = messageLock

  def add_to_message_table(self, listOfMessages: list[int]) -> None:
    '''Adds messages to the saved list, assumes lock is held'''
    for message in listOfMessages:
      self.messagesObtained.add(message)


  def extract_steam_of_messages(self) -> list[int]:
    '''Extracts the current stream of messages, assumes lock is held'''
    messages = []
    while self.curKey in self.messagesObtained:
      messages.append(self.curKey)
      self.messagesObtained.discard(self.curKey)
      self.curKey += 1
    return messages

  def process(self, messages: list[int]) -> None:
      '''Recieves a list of messages and invokes the processor when a stream of messages comes in'''
      self.lock.acquire()
      self.add_to_message_table(messages)
      if self.curKey in self.messagesObtained:
        messages = self.extract_steam_of_messages()
        self.processor.process(messages)
      self.lock.release()
      

if __name__ == "__main__":
  processor = DriverProcessor()
  messagesObtained = set()
  lock = Lock()
  listener = collatingListener(processor, messagesObtained, lock)

  # Example code
  listener.process([1,4])
  listener.process([0])
  listener.process([2])
  listener.process([3,5,6,7])

