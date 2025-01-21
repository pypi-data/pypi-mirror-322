import os

def __init__():
    print('Hello, this is better print.')

def clear_console():
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

def print_massage(message):
    clear_console()
    print(message)

def draw_line(length):
    print('-'*length)

def draw_dog():
    print("""
     /\\__/\\
  __/  O O   | 
O            |
  ------------
    """)