def help() -> None:
    '''
    Вывод информации о доступных командах и их опциях
    :return: Данная функция ничего не возвращает
    '''
    print('''Доступные команды:

ls [-l] [путь]              - список файлов и директорий
cd [путь]                   - сменить текущую директорию
cat файл                    - вывести содержимое файлов
cp [-r] ист цель            - копировать файлы/директории
mv ист цель                 - переместить или переименовать
rm [-r] файл                - удалить файл/директорию
zip файл архив.zip          - создание архива ZIP
unzip архив.zip             - распаковка архива ZIP
tar файл архив.tar.gz       - создание архива TAR.GZ
untar архив.tar.gz          - распаковка архива TAR.GZ
grep [-r] [-i] шаблон файл  - поиск строк, соответствующих шаблону
undo                        - отменить последнюю операцию
history [количество]        - вывод истории введённых команд

~                  - домашняя директория
..                 - родительская директория
.                  - текущая директория\n''')
    
    print('''Available commands:

ls [-l] [path]               - list directory contents
cd [path]                    - change current directory
cat [file]                   - display file contents
cp [-r] src dest             - copy files/directories
mv src dest                  - move or rename files/directories
rm [-r] file                 - remove files/directories
zip file archive.zip         - create a ZIP archive
unzip archive.zip            - unpack ZIP archive
tar file archive.tar.gz      - craete a TAR.GZ archive
untar archive.tar.gz         - unpack TAR.GZ archive
grep [-r] [-i] pattern file  - search for strings matching a pattern
undo                         - undo last operation
history [amount]             - display list of used commands

~                  - home directory
..                 - parent directory
.                  - current directory''')