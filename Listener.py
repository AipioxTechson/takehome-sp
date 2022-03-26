from abc import ABC, abstractmethod

from Processor import Processor


class Listener(ABC):
  '''Abstract model for a Collating Listener'''

  def __init__(self, processor: Processor) -> None:
    self.processor = processor
    super().__init__()

  abstractmethod
  async def process(self, messages: list[int]) -> None:
    '''Recieves a list of messages and invokes the processor when a stream of messages comes in'''
    pass
