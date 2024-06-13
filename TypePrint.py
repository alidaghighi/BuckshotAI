import time
import random

@staticmethod
def typePrint(m):
    l = list(m)
    for i in range(0, len(l)):
        print(l[i], end='', flush=True)
        randomTime = random.uniform(0, 1)
        if randomTime < 0.7:
            t = 0.02
        else:
            t = 0.1
        time.sleep(t)
    print()
