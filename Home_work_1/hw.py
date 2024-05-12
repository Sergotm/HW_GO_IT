from pathlib import Path
from shutil import copyfile
from threading import Thread
import time


def read_folder(path: Path) -> None:
    for element in path.iterdir():
        if element.is_dir():  # TODO перевірка чи є папкою
            read_folder(element)
        else:
            copy_file(element)  # TODO функція для копіювання файлів


def copy_file(file: Path) -> None:
    ext = file.suffix
    new_path = output_folder / ext
    new_path.mkdir(parents=True, exist_ok=True)
    copyfile(file, new_path / file.name)


if __name__ == '__main__':
    output_folder = Path('dist')
    start = time.time()
    path = Path('Picture')
    for i in range(1):
        th = Thread(target=read_folder(path))
        th.start()

    stop = time.time()
    result = stop - start
    print(f'End program. Result time {result}')
    #  TODO  0.0327608585357666


# if __name__ == '__main__':
#     output_folder = Path('dist')
#     start = time.time()
#     read_folder(Path('Picture'))
#     stop = time.time()
#     result = stop - start
#     print(f'End program. Result time {result}')

    # TODO 0.015247344970703125