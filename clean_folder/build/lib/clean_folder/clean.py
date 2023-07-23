import shutil
import sys
import re
from pathlib import Path

IMG = ('JPEG', 'PNG', 'JPG', 'SVG')
VIDEO = ('AVI', 'MP4', 'MOV', 'MKV')
DOC = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
MUSIC = ('MP3', 'OGG', 'WAV', 'AMR')
ARH = ('ZIP', 'GZ', 'TAR')

finded_files_suffix = set()
dont_know_suffix = set()
folders = []
folders_for_delete = []

list_images = []
list_videos = []
list_docs = []
list_musics = []
list_arhives = []
list_other = []

not_scan_dir = ("archives", "video", "audio", "documents", "images")


# test ================

def greeting():
    print("Hello World")


# test ================


# перебор папок и файлов
def search_files(path) -> None:
    p = Path(path)
    for i in p.iterdir():
        if i.name == '.DS_Store':
            continue
        if i.is_dir():
            if i.name not in not_scan_dir:
                folders_for_delete.append(i)
                folders.append(normalize(i.name))
                search_files(i)
        if i.is_file():
            marker_files(i)


# Поиск файлов по категориям
def marker_files(path) -> None:
    suffix = path.suffix.upper()[1:]
    if suffix in IMG:
        list_images.append(normalize(path.name))
        finded_files_suffix.add(suffix)
        move_files(path, path_resolve / "images")
    elif suffix in VIDEO:
        list_videos.append(normalize(path.name))
        finded_files_suffix.add(suffix)
        move_files(path, path_resolve / "video")
    elif suffix in DOC:
        list_docs.append(normalize(path.name))
        finded_files_suffix.add(suffix)
        move_files(path, path_resolve / "documents")
    elif suffix in MUSIC:
        list_musics.append(normalize(path.name))
        finded_files_suffix.add(suffix)
        move_files(path, path_resolve / "audio")
    elif suffix in ARH:
        list_arhives.append(normalize(path.name))
        finded_files_suffix.add(suffix)
        move_files(path, path_resolve / "archives", arhives=True)
    else:
        list_other.append(normalize(path.name))
        dont_know_suffix.add(suffix)
        move_files(path, path_resolve / "other")


def move_files(path, dir, arhives=False) -> None:
    dir.mkdir(exist_ok=True, parents=True)
    if arhives == False:
        path.replace(dir / normalize(path.name))
    else:
        arhives_folder = dir / normalize(path.name.replace(path.suffix, ''))
        arhives_folder.mkdir(exist_ok=True, parents=True)
        shutil.unpack_archive(path, arhives_folder)


def delete_folder():
    for i in folders_for_delete:
        try:
            i.rmdir()
        except OSError:
            print(f"Не удалось удалить папку {i}")


# переименовывание папок и файлов и уделение ненужных символов
def normalize(name: str) -> str:
    CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
    TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    try:
        index = name.find(".")
        norm_name = name[:index]
        sufix = name[index:]
        norm_name = norm_name.translate(TRANS)
        norm_name = re.sub(r'\W', '_', norm_name)
        return norm_name + sufix
    except:
        name = name.translate(TRANS)
        name = re.sub(r'\W', '_', name)
        return name

def start():
    if len(sys.argv) != 2:
        print("Не передана папка для поиска и сортировки файлов!")
    else:
        path_resolve = Path(sys.argv[1]).resolve()
        search_files(path_resolve)
        print(f"Результати пошуку у папці: {sys.argv[1]}")
        print("")
        print("Список усіх знайдених файлів: ")
        print(f"Images: {list_images}")
        print(f"Videos: {list_videos}")
        print(f"Docs: {list_docs}")
        print(f"Musics: {list_musics}")
        print(f"Arhives: {list_arhives}")
        print(f"Інші файли: {list_other}")
        print("")
        print(f"Список відомих розширень файлів: {finded_files_suffix}")
        print("")
        print(f"Список НЕ відомих розширень файлів: {dont_know_suffix}")
        print("")
        print(f"Список усіх знайдених папок: {folders}")
        delete_folder()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Не передана папка для поиска и сортировки файлов!")
    else:
        path_resolve = Path(sys.argv[1]).resolve()
        search_files(path_resolve)
        print(f"Результати пошуку у папці: {sys.argv[1]}")
        print("")
        print("Список усіх знайдених файлів: ")
        print(f"Images: {list_images}")
        print(f"Videos: {list_videos}")
        print(f"Docs: {list_docs}")
        print(f"Musics: {list_musics}")
        print(f"Arhives: {list_arhives}")
        print(f"Інші файли: {list_other}")
        print("")
        print(f"Список відомих розширень файлів: {finded_files_suffix}")
        print("")
        print(f"Список НЕ відомих розширень файлів: {dont_know_suffix}")
        print("")
        print(f"Список усіх знайдених папок: {folders}")
        delete_folder()
