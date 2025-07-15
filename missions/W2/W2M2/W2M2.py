from multiprocessing import Process

def print_continent(name = 'Asia'):
    print(f'The name of continent is : {name}')


if __name__ == '__main__':
    continents = ['America', 'Europe', 'Africa']
    processes = []
    p = Process(target = print_continent)
    p.start()
    processes.append(p)
    for continent in continents:
        p = Process(target = print_continent, args = (continent, ))
        p.start()
        processes.append(p)
    for process in processes:
        process.join()