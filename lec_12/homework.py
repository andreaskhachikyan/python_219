import random
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)  # Call the original function
        end = time.time()
        print(f'{func.__name__} method execution time: {end - start}')
        return result
    return wrapper


@timer
def createFile():
    with open('num.txt', 'w') as file:
        for _ in range(100):
            randNums = [str(random.randint(0, 100)) for _ in range(20)]
            file.write(' '.join(randNums))
            file.write('\n')


@timer
def filterFile():
    with open('num.txt', 'r') as file:
        lines = file.readlines()
        lines = map(lambda line: [int(i) for i in line.split()], lines)
        lines = list(map(lambda line: filter(lambda i: i > 40, line), lines))

    with open('num.txt', 'w') as file:
        for line in lines:
            file.write(' '.join([str(i) for i in line]))
            file.write('\n')


@timer
def readAsGenerator():
    with open('num.txt', 'r') as file:
        for line in file:
            yield line


createFile()
filterFile()

fileGen = readAsGenerator()
print(fileGen)
for line in fileGen:
    print(line.strip())
