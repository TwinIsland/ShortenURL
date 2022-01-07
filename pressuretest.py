import random
import ShortURL
import time

func = ShortURL.ShortURL()


def generate_url():
    result = ""
    for ii in range(10):
        result += chr(random.randint(ord('a'), ord('z'))) if random.randint(0, 1) else str(random.randint(0, 9))
    return "https://" + result + ".com"


# write test
time_s = time.time()
for i in range(1000):  # 1.7s, safe mode
    func.add(generate_url())
time_e = time.time()

func.close()
print(func.len())
print(time_e - time_s)
