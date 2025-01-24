import comtypes.client # pip install comtypes
from pymediainfo import MediaInfo # pip install pymediainfo
from datetime import datetime
from os import walk
from os.path import getsize, getctime, dirname, basename
import tkinter as tk
from tkinter import filedialog

from prophet_tools.terminal import print_in_color
from prophet_tools.my_functions import check_in

SHELL = comtypes.client.CreateObject("Shell.Application")
PROPERTIES = {
        "size": 1,
        "type": 2,
        "changed": 3,
        "created": 4,
        "len": 27,
        "created_clean": 208,
        "bitrate": 313,
        "width": 314,
        "fps": 315,
        "height": 316,
    }

def files_list(path, subfolders=False, paths_only=False):
    class File:
        def __init__(self, file, folder) -> None:
            self.full_name = file
            self.name = self.full_name.rsplit('.', 1)[0]
            self.ext = self.full_name.rsplit('.', 1)[-1]
            self.path = f'{folder}\\{file}'
            self.folder_path = folder
            self.folder_name = folder.rsplit('\\', 1)[-1]
        #     self.get_properties()

        # def get_properties(self):
        #     if not properties:
        #         self.properties = {}
        #         return

        #     self.properties = {}
        #     if 'size' in properties:
        #         self.properties['size'] = round(getsize(self.path) / 1000000, 1)

        #     if 'creation' in properties:
        #         creation_time = getctime(self.path)
        #         creation_date = datetime.fromtimestamp(creation_time)
        #         self.properties['creation'] = creation_date

        #     shell = comtypes.client.CreateObject("Shell.Application")
        #     ns = shell.NameSpace(dirname(self.path))
        #     item = ns.ParseName(basename(self.path))
        #     bit_rate = ns.GetDetailsOf(item, 284)
        #     width = ns.GetDetailsOf(item, 26)

            # if check_in(['bitrate', 'width', 'height', 'frame_rate'], properties):
            #     media_info = MediaInfo.parse(self.path)
            #     found = False
            #     for track in media_info.tracks:
            #         if track.track_type == 'Video':
            #             bit_rate = track.bit_rate
            #             width = track.width
            #             height = track.height
            #             frame_rate = track.frame_rate
            #             found = True
            #             break

            #     if found:
            #         self.properties['bitrate'] = round(bit_rate / 1000000, 2)
            #         self.properties['width'] = width
            #         self.properties['height'] = height
            #         self.properties['frame_rate'] = frame_rate
            #         print(f'{self.name} -- {self.properties['bitrate']}')

    предварительный_список = list(walk(path))
    if len(предварительный_список) == 0:
        # print_in_color('Такой папки не существует', red=True)
        return []

    if subfolders:
        все_папки = предварительный_список
    else:
        все_папки = [предварительный_список[0]]

    res = []
    for список in все_папки:
        корневая_папка = список[0]
        файлы = список[2]
        if paths_only:
            for файл in файлы:
                res.append(f'{корневая_папка}\\{файл}')
            continue

        for файл in файлы:
            res.append(File(файл, корневая_папка))

    return res

def get_property_for_one_file(file_path: str, properties: list):
    if '/' in file_path:
        file_path = file_path.replace('/', '\\')
    folder_path = dirname(file_path)
    full_name = basename(file_path)
    ns = SHELL.NameSpace(folder_path)
    item = ns.ParseName(full_name)

    result = {}
    for prop in properties:
        if prop in PROPERTIES:
            this_property = ns.GetDetailsOf(item, PROPERTIES[prop])
            if prop == 'size':
                number, rate = this_property.split()
                number = float(number.replace(',', '.'))
                if rate == 'КБ':
                    number /= 1000
                elif rate == 'ГБ':
                    number *= 1000
                elif rate == 'ТБ':
                    number *= 1000000
                result[prop] = number
            elif prop == 'bitrate':
                number = this_property.split(' ', 1)[0]
                number = number.replace('\u200e', '')
                result[prop] = number
            else:
                result[prop] = this_property

    return result

def get_properties(files, properties):
    if type(files) is str:
        result = get_property_for_one_file(files, properties)
        return result
    else:
        for file in files:
            result = get_property_for_one_file(file.path, properties)
            file.propetries = result


def choose_folder_dialog(initial_folder=None):
    root = tk.Tk()
    root.withdraw()  # Скрыть основное окно Tkinter

    folder_path = filedialog.askdirectory(initialdir=initial_folder)  # Открыть диалоговое окно выбора папки

    return folder_path


if __name__ == '__main__':
    print(get_property_for_one_file(r"C:\Users\User\AppData\Roaming\PotPlayerMini64\Playlist\house of the dragon.dpl", ['changed']))
