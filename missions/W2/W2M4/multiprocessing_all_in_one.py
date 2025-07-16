from multiprocessing import Process, Queue
import queue
import time
SENTINEL = '__end__'
def task(task_todo, task_done, i):
    while True:
        try:
            t = task_todo.get_nowait()
            if t == SENTINEL:
                break
            else:
                print(f'Task no {t}')
                time.sleep(0.5)
                task_done.put((t, i))
        
        except queue.Empty:
            continue

if __name__ == '__main__':
    tasks_that_to_accomplish = Queue()
    tasks_that_are_done = Queue()

    tasks = [i for i in range(10)]
    for t in tasks:
        tasks_that_to_accomplish.put(t)
        
    for _ in range(4):
        tasks_that_to_accomplish.put(SENTINEL)

    processes = [Process(target=task, args=(tasks_that_to_accomplish, tasks_that_are_done, i+1)) for i in range(4)]

    for process in processes:
        process.start()
    
    for process in processes:
        process.join()
    
    while not tasks_that_are_done.empty():
        task_num, process_num = tasks_that_are_done.get()
        print(f'Task no {task_num} is done by Process-{process_num}')
    
