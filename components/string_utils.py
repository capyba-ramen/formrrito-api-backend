import random
import time

import base58


def b58_hash_time(encoding='utf-8'):
    time_now = time.time()
    random_num = random.random()

    base58_encoded_int = base58.b58encode_int(int(time_now * 10000) * 10000 + int(random_num * 10000))

    return base58_encoded_int.decode(encoding)


print(b58_hash_time())
