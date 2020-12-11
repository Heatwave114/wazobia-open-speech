import tensorflow as tf
from termcolor import colored

def check_gpu():
  gpu_count = len(tf.config.experimental.list_physical_devices('GPU'))
  if gpu_count == 0:
    print(colored('*****WARNING! No GPUs detected [If in colab change runtime type to GPU]*****', 'red'))

if __name__ == '__main__':
  check_gpu()
