import multiprocessing, logging
from multiprocessing import Pool, current_process, cpu_count
from time import time


def factorize(*number):
    new_list = []
    for element in number:
        rezult = []
        for el in range(1, element + 1):
            if element % el == 0:
                rezult.append(el)
        new_list.append(rezult)
    print(f'{current_process().name}')
    return new_list


def callback(rezult):
    print(f'End {current_process().name}')


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(mesasage)s')
    count_cpu = 2
    start_1 = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    number = [128, 255, 99999, 10651060]
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
    1521580, 2130212, 2662765, 5325530, 10651060]

    print(f'Синхронне виконалось')
    print(f'Резульатат {time()-start_1}')
    start_2 = time()
    with Pool(count_cpu) as pool:
        print(f'Count CPU: {cpu_count()}')
        print(f'Ми використовуємо {count_cpu}')
        rezults = pool.map_async(factorize, number, callback=callback)
        rezults.get()
        pool.close()
        pool.join()

    print(f'Ми виконали через Process часу пішло: {time()-start_2}')

    start_3 = time()
    with multiprocessing.Pool() as pool:
        rezults = pool.map_async(factorize, number, callback=callback)
        rezults.get()
        pool.close()
        pool.join()

    print(f'Ми виконали через multiProcessing часу пішло: {time() - start_3}')
