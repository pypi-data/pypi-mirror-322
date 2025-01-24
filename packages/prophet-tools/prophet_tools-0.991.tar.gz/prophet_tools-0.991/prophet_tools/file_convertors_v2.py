# pip install pillow-avif-plugin Pillow
from os import remove
from PIL import Image
import pillow_avif
from prophet_tools.terminal import print_in_color
from prophet_tools.file_info import files_list

def convert_CR2_to_JPG(path_from, path_to):
    image = Image.open(path_from)
    width, height = image.size
    rgb_image = image.convert('RGB')
    rgb_image.resize((width, height))
    rgb_image.save(path_to)
    name = path_from.rsplit("\\")[-1]
    print_in_color(f'{name}', blue=True)
    image.close()

def resize_one_image(path, lim=2500, output=None):
    try:
        image = Image.open(path)
    except:
        print_in_color(f'Не получается открыть файл "{path}"', red=True)
        return None
    width, height = image.size

    if width <= lim and height <= lim and not output:
        return path

    if output:
        path = output
    ratio = width/height
    if width > height:
        width = lim
        height = int(width/ratio)
    else:
        height = lim
        width = int(height*ratio)

    new_image = image.resize((width, height))
    if path.rsplit('.', 1)[-1] != 'png':
        new_image = new_image.convert('RGB')

    image.close()
    try:
        new_image.save(path)
    except Exception as error:
        print_in_color(f'''Картинка не может быть сохранена.
{path}
{error}''', red=True)
        raise error
    name = path.rsplit("\\")[-1]
    print_in_color(f'{name}', blue=True)
    return path

def resize_folder(path, lim=2500):
    files = files_list(path, subfolders=True)

    for file in files:
        if file.ext.lower() not in ['png', 'webp', 'jpeg', 'jpg', 'cr2', 'avif']:
            continue
        old_path = file.path

        if file.ext.lower() in ['webp', 'cr2', 'avif']:
            correct_ext = '.jpg'
            delete_original = old_path
        else:
            correct_ext = '.' + file.ext
            delete_original = None
        new_path = file.folder_path + '\\' + file.name + correct_ext

        if file.ext.lower() == 'cr2':
            convert_CR2_to_JPG(old_path, new_path)
        else:
            resize_one_image(old_path, lim, new_path)

        if delete_original:
            remove(old_path)

def ffmpeg_merge_files(video_source,audio_source):
    import subprocess
    import os

    if not os.path.exists('C:/ffmpeg.exe'):
        raise ValueError('не найден файл C:/ffmpeg.exe')
    output_source = video_source + "merged.mp4"
    print('=== ffmpeg merging')
    subprocess.run(f"C:/ffmpeg.exe -i {video_source} -i {audio_source} -c copy {output_source}")
    os.remove(video_source)
    os.remove(audio_source)
    os.rename(output_source, video_source)
    print('=== ffmpeg merge complete')

if __name__ == "__main__":
    size = input("MAX SIZE OR FOLDER: ")
    if size.isnumeric():
        size = int(size)
        path = input("Ссылка на папку: ")
    else:
        path = size
        size = 2500
    resize_folder(path, size)