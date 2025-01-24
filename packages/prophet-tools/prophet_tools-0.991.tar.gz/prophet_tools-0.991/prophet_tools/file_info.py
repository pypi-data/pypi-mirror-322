import comtypes.client # pip install comtypes
from pymediainfo import MediaInfo # pip install pymediainfo
from datetime import datetime
from os import walk
from os.path import getsize, getctime, dirname, basename
from terminal import print_in_color
from my_functions import check_in

def files_list(path, subfolders=False, paths_only=False):
    class File:
        def __init__(self, file, folder) -> None:
            self.full_name = file
            self.name = self.full_name.split('.', 1)[0]
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

def get_properties(files, properties):
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
    shell = comtypes.client.CreateObject("Shell.Application")

    for file in files:
        ns = shell.NameSpace(file.folder_path)
        item = ns.ParseName(file.full_name)

        file.properties = {}
        for prop in properties:
            if prop in PROPERTIES:
                this_property = ns.GetDetailsOf(item, PROPERTIES[prop])
                if prop == 'size':
                    number, rate = this_property.split()
                    number = int(number)
                    if rate == 'КБ':
                        number /= 1000
                    elif rate == 'ГБ':
                        number *= 1000
                    elif rate == 'ТБ':
                        number *= 1000000
                    file.properties[prop] = number
                elif prop == 'bitrate':
                    number = this_property.split(' ', 1)[0]
                    number = number.replace('\u200e', '')
                    file.properties[prop] = number
                else:
                    file.properties[prop] = this_property
        print(file.name)

if __name__ == '__main__':
    res = files_list(r'D:\Looper movies')
    get_properties(res, ['bitrate'])
    txt = ''
    for file in res:
        txt += f'{file.name} -- {file.properties.get("bitrate")}\n'

    with open('c:/dev/exchange/list of movies.txt', encoding='utf-8', mode='w') as file:
        file.write(txt)

    print('done')
