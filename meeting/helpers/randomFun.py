
import string
import random

def getRandomIntNumber():
    # choose from [0-9]
    num = string.digits
    result_str = ''.join(random.choice(num) for i in range(4))
    return result_str

def getRandomCharID():
    # choose from [0-9], [a-z], [A-Z]
    num = string.digits
    result_str = ''.join(random.choice(num) for i in range(4))
    return result_str


