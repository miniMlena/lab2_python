def help() -> None:
    '''
    Вывод информации о доступных командах и их опциях
    :return: Данная функция ничего не возвращает
    '''
    print('''Доступные команды:

ls [путь]                   - список файлов и директорий
ls -l [путь]                - подробный список (права, размер, дата изменения)
cd [путь]                   - сменить текущую директорию
cat [файл...]               - вывести содержимое файлов
cp [-r] ист цель            - копировать файлы/директории
mv ист цель                 - переместить или переименовать
rm [-r] файл                - удалить файл/директорию
grep [-r] [-i] шаблон файл  - поиск строк, соответствующих шаблону

~                  - домашняя директория
..                 - родительская директория
.                  - текущая директория\n''')
    
    print('''Available commands:

ls [path]                    - list directory contents
ls -l [path]                 - long listing (permissions, size, modification date)
cd [path]                    - change current directory
cat [file...]                - display file contents
cp [-r] src dest             - copy files/directories
mv src dest                  - move or rename files/directories
rm [-r] file...              - remove files/directories
grep [-r] [-i] pattern file  - search for strings matching a pattern

~                  - home directory
..                 - parent directory
.                  - current directory''')