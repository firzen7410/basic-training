import threading
import time


def worker(name):
    for i in range(3):
        print(f"Thread {name}: {i}")
        time.sleep(1)


t1 = threading.Thread(target=worker, args=("A",))
t2 = threading.Thread(target=worker, args=("B",))

t1.start()
t2.start()
t1.join()
t2.join()
