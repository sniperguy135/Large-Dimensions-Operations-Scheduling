
import multiprocessing
from multiprocessing import Process


#
# MULTIPROCESSING TEST
#

def func1(return_dict):
    print("func1: starting")
    for i in range(10**3):
        i/2

    print("func1: finishing")
    #return equivalent
    return_dict['func1'] = "This comes from function 1"


def func2(return_dict):
    print("func2: starting")
    for i in range(10**6):
        i//4

    print("func2: finishing")
    return_dict['func2'] = "Function 2 says hi"

def func3(return_dict):
    print("func3: starting")
    for i in range(10**7):
        i%3

    print("func3: finishing")
    return_dict['func3'] = "Function 3's a crowd"

def func4(return_dict):
    print("func4: starting")
    for i in range(10**4):
        i**0.5

    print("func4: finishing")
    return_dict['func4'] = "Did function 4 check in?"


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    p1 = Process(target=func1, args=(return_dict,))
    p1.start()
    p2 = Process(target=func2, args=(return_dict,))
    p2.start()
    p3 = Process(target=func3, args=(return_dict,))
    p3.start()
    p1.join()
    p2.join()
    p4 = Process(target=func4, args=(return_dict,))
    p4.start()
    p3.join()
    p4.join()

    print(return_dict)
