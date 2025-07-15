from multiprocessing import Pool
import time

def work(work):
    work_name, work_time = work
    print(f'Process {work_name} waiting {work_time} seconds')
    time.sleep(work_time)
    print(f'Process {work_name} Finished.')

if __name__ == '__main__':
    workers = [('A', 5), ('B', 2), ('C', 1), ('D', 3)]
    with Pool(2) as p:
        p.map(work, workers)