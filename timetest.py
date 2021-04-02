import time

start = time.time()
def millis():
    return round((time.time()- start) * 1000)

state = False

while True:
    print(millis() / 1000)


