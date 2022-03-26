from threading import Lock

from Listener import CollatingListener
from Processor import MockProcessor

def setup_mock(expected_list: list[list[int]]):
  '''Provides the basic setup for a mock implementation'''

  processor = MockProcessor(expected_list)
  messages_obtained = set()
  lock = Lock()
  listener = CollatingListener(processor, messages_obtained, lock)

  return listener

def execute_test(listener: CollatingListener, list_of_messages: list[list[int]]):
  '''Provides the basic setup for executing a test'''
  
  for messages in list_of_messages:
    listener.process(messages)


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

  execute_test(setup_mock(expected_list),messages)

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