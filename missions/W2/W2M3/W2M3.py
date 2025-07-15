from multiprocessing import Process, Queue

SENTINEL = '__end__'

def Push(q, items):
    print('pushing items to queue:')
    for i, item in enumerate(items):
        q.put(item)
        print(f'item no: {i+1} {item}')
    q.put(SENTINEL)

def Pop(q):
    i = 0
    print('popping items from queue:')
    while True:
        item = q.get()
        if item == SENTINEL:
            break
        print(f'item no: {i} {item}')
        i += 1


if __name__ == '__main__':
    q = Queue()
    data = ['red', 'green', 'blue', 'black']

    pushing = Process(target = Push, args = (q, data))
    popping = Process(target = Pop, args = (q, ))

    pushing.start()
    pushing.join()

    popping.start()
    popping.join()