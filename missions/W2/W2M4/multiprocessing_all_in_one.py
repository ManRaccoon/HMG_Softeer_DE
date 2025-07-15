# from multiprocessing import Process, Queue
# import time

# def task():
    



# if __name__ == '__main__':
#     tasks_that_to_accomplish = Queue()
#     tasks_that_are_done = Queue()

#     taskNum = [i for i in range(10)]
#     p1 = Process(target=task, args=(taskNum,), name='Process-1')
#     p2 = Process(target=task, args=(taskNum,), name='Process-2')
#     p3 = Process(target=task, args=(taskNum,), name='Process-3')
#     p4 = Process(target=task, args=(taskNum,), name='Process-4')
    
#     processes = [p1, p2, p3, p4]

#     for process in processes:
#         process.start()
    
#     for process in processes:
#         process.join()
    
