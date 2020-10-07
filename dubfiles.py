import os, sys
import hashlib


def findDup(parentFolder):
    # Дубликаты в формате {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print('Сканируем %s...' % dirName)
        for filename in fileList:
            # получаем полный путь к файлу.
            path = os.path.join(dirName, filename)
            # считаем хэш-сумму
            file_hash = hashfile(path)
            # добавляем путь к файлу в созданный ранее пустой словарь
            # Если хэш уже есть в словаре, добавляем его снизу
            # иначе добавляем как есть
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups


# Если папок для поиска дубликатов несколько, используем фукцию объединения словарей
def joinDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]


# Функция подсчета хеш-суммы файлов, размер хеша - 8кбайт (65536 байта)
def hashfile(path, blocksize=65536):
    afile = open(path, 'rb')
    # создание словаря хэшей
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


# Выдача результата. Результат - лист со значениями словаря
def printResults(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if len(results) > 0:
        print('Найденные дубликаты:')
        print('Данные файлы идентичны. Имя файла может отличаться, но содержимое одинаково')
        print('___________________')
        for result in results:
            for subresult in result:
                print('\t\t%s' % subresult)#
            print('___________________')

    else:
        print('Дубликаты не найдены')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        dups = {}
        folders = sys.argv[1:]
        for i in folders:
            if os.path.exists(i):
                joinDicts(dups, findDup(i))
            else:
                print('%s Неправильный путь к файлам' % i)
                sys.exit('Попробуйте снова')# выход из питона
        printResults(dups)
    else:
        print('Использование: python dupFinder.py folder or python dupFinder.py folder1 folder2 folder3')