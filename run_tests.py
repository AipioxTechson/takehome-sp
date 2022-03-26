from threading import Lock
import random

from Listener import CollatingListener
from Processor import MockProcessor

def test_example():
  '''Runs example test code'''
  expected_list = [
    [0,1],
    [2],
    [3,4,5,6,7]
  ]

  messages = [ 
    [1,4],
    [0],
    [2],
    [3,5,6,7]
  ]

  listener, _ = setup_mock(expected_list)

  execute_test(listener,messages)

def test_no_call():
  '''Tests no process calls, This is an error case since we usually assume all messages will be recieved'''
  expected_list = []
  messages = [ 
    [1,4],
    [2],
    [3,5,6,7]
  ]
  listener, processor = setup_mock(expected_list)

  execute_test(listener, messages)

  assert processor.times_called == 0, "Process was never called"

def test_full_message():
  '''Tests all N messages arrive in 1 shot, given random ordering and parititions, STRESS TEST'''

  N = random.randint(10,20)

  expected_messages = list(range(0,N))


  list_of_messages = expected_messages[1:]
  random.shuffle(list_of_messages)

  messages = random_paritition(list_of_messages)

  listener, processor = setup_mock([expected_messages])

  execute_test(listener,messages)

  assert processor.times_called == 0, "No calls were made"

  listener.process([0])

def test_single_messages():
  '''Tests N messages arriving in sequence, STRESS TEST'''

  N = random.randint(10,20)

  expected_messages = list(range(0,N))

  messages = random_paritition(expected_messages)

  listener, _ = setup_mock(messages)

  execute_test(listener,messages)




#Setup

def random_paritition(list_of_messages: list[int]) -> list[list[int]]:
  '''Randomly partitions messages'''
  messages = []

  messages_to_be_parsed = len(list_of_messages)
  messages_parsed = 0

  while messages_to_be_parsed != 0:
    chunk_size = random.randint(1,messages_to_be_parsed)
    messages.append(list_of_messages[messages_parsed: messages_parsed + chunk_size])
    messages_parsed += chunk_size
    messages_to_be_parsed -= chunk_size
  return messages


def setup_mock(expected_list: list[list[int]]):
  '''Provides the basic setup for a mock implementation'''

  processor = MockProcessor(expected_list)
  messages_obtained = set()
  lock = Lock()
  listener = CollatingListener(processor, messages_obtained, lock)

  return listener, processor

def execute_test(listener: CollatingListener, list_of_messages: list[list[int]]):
  '''Provides the basic setup for executing a test'''
  
  for messages in list_of_messages:
    listener.process(messages)


def run_tests():
  """
    Runs all tests in this file
  """
  passed, failed = [], []
  for name, func in globals().items():
    if name.startswith('test') and callable(func):
      try:
        func()
        print(f'{name} Passed')
      except Exception as err:
        failed.append(f'{name}: {str(err)}')
        continue
      passed.append(name)
  if not failed:
      print(f'All {len(passed)} tests passed.')
  else:
      print(f'Total {len(passed) + len(failed)} tests, failed {len(failed)}:')
      for test in failed:
          print(test)
      exit(1)


if __name__ == '__main__':
    run_tests()