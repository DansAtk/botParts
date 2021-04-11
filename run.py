from core import *
from ext import *

def main():
    try:
        while True:
            input_text = input()
            
            trigger = None

            try:
                trigger = config.settings['trigger']

            except KeyError:
                pass

            commandM.read(input_text, trigger)
    finally:
        contrigM.moduleCleanup()

if __name__ == "__main__":
    main()

else:
    print("Run this as main")
