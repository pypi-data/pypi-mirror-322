"""
This is dummy code to test CI functions
"""

import random

def chose_num() -> int:
    return random.choice([1,2,3,4,5])

def double_num(num:int):
    return num*2

def main():
    num = chose_num()
    num = double_num("hello")
    print(num)

if __name__ == '__main__':
    main()