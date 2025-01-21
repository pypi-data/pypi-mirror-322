import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from FusionX.example import hello
if __name__ == "__main__":
    hello() == "hello"
