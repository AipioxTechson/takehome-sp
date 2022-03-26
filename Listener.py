from abc import ABC, abstractmethod
from threading import Lock, Thread
import time

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


class CollatingListener(Listener):
  '''
  This class represents the implementation for a Listener
  '''
  def __init__(self, processor: Processor, messages_obtained: set[int], message_lock: Lock):
    super().__init__(processor)
    self.cur_key = 0
    self.messages_obtained = messages_obtained
    self.lock = message_lock

  def add_to_message_table(self, listOfMessages: list[int]) -> None:
    '''Adds messages to the saved list, assumes lock is held'''

    for message in listOfMessages:
      self.messages_obtained.add(message)


  def extract_steam_of_messages(self) -> list[int]:
    '''Extracts the current stream of messages, assumes lock is held'''

    messages = []
    while self.cur_key in self.messages_obtained:
      messages.append(self.cur_key)
      self.messages_obtained.discard(self.cur_key)
      self.cur_key += 1
    return messages

  def process(self, messages: list[int]) -> None:
      '''Recieves a list of messages and invokes the processor when a stream of messages comes in'''
      self.lock.acquire()
      self.add_to_message_table(messages)
      if self.cur_key in self.messages_obtained:
        messages = self.extract_steam_of_messages()
        self.processor.process(messages)
      self.lock.release()
      

def driverCode(listener, expected_list_of_messages,ID):
  '''Multi threaded driver code'''

  for message in expected_list_of_messages:
    print(f'{ID} PROCESSING', message)
    listener.process(message)
    

if __name__ == "__main__":
  processor = DriverProcessor()
  messages_obtained = set()
  lock = Lock()
  listener = CollatingListener(processor, messages_obtained, lock)

  # Example code
  listener.process([1,4])
  listener.process([0])
  listener.process([2])
  listener.process([3,5,6,7])

  # #Multi threaded example code
  # processor = DriverProcessor()
  #messages_obtained = set()
  # lock = Lock()
  # listener1 = CollatingListener(processor, messages_obtained, lock)
  # listener2 = CollatingListener(processor, messages_obtained, lock)
  
  # t1 = Thread(target=driverCode,args=(listener1, [[1,4],[2]],'1'))
  # t2 = Thread(target=driverCode,args=(listener2, [[0],[3,5,6,7]],'2'))

  # t1.start()
  # t2.start()

  # t2.join()
  # t1.join()


