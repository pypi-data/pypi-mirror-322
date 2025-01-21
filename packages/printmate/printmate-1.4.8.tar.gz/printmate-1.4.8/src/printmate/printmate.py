import time
import sys
from colorama import Fore, Style
from colorama import init

# Initialize colorama
init()

class primate:
    @staticmethod
    def print(text, speed=1, color=Fore.WHITE):
        for char in text:
            sys.stdout.write(color + char + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(1/speed)
        print()
