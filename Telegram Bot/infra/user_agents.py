import random
UAS = [
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Mobile Safari/537.36",
    "okhttp/4.9.0",  # some mobile apps use okhttp UA
    "Dalvik/2.1.0 (Linux; U; Android 10; SM-G960F Build/QP1A)",
]
def random_ua():
    return random.choice(UAS)
