from shutil import make_archive, copytree, copy2, rmtree, unpack_archive
from tkinter.messagebox import showinfo
from os import mkdir, rename, remove, urandom
from tkinter import Tk, Button
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox
from sys import platform
from _locale import _getdefaultlocale

class BRP_PACKER:
    __slots__ = ['bootanimation', 'file_dont_selected', 'archive_maked',
                 'select_file_text', 'make_archive_text', 'window',
                 'type_of_archive']

    def __init__(self):
        self.bootanimation = False
        unpack_archive('resources.zip')
        self.make_lang()
        self.main_window()

    def make_lang(self):
        locale_str = _getdefaultlocale()[0].split('_')[0]
        lang_pack = open('lang_pack.brp', 'r', encoding='utf-8').readlines()
        line_index = [index for index in range(
            0, len(lang_pack), 5) if lang_pack[index].strip() == locale_str][0]
        self.file_dont_selected = lang_pack[line_index + 1].strip()
        self.archive_maked = lang_pack[line_index + 2].strip()
        self.select_file_text = lang_pack[line_index + 3].strip()
        self.make_archive_text = lang_pack[line_index + 4].strip()
        

    def del_temp(self):
        dirs = ['./temp', './programm_resources',
            './Splash', './Bootanimation', '__pycache__']
        for dir_ in dirs:
            try:
                rmtree(dir_)
            except:
                pass

    def make_bootanimation_archive(self):
        if not self.bootanimation:
            showinfo(title='Warning!', message=self.file_dont_selected)
            return
        bootanimation_temp = self.bootanimation.split('/')[-1]
        file_type = self.type_of_archive.get()
        mkdir('./temp')
        copy2(self.bootanimation, './temp')
        copytree('./programm_resources', './bootanimation_archive')
        if file_type == 'Splash':
            rename(f'./temp/{bootanimation_temp}', './temp/Splash.img')
            self.bootanimation = './temp/Splash.img'
            copy2(self.bootanimation, './bootanimation_archive')
        else:
            rename(f'./temp/{bootanimation_temp}',
                   './temp/bootanimation.zip')
            self.bootanimation = './temp/bootanimation.zip'
            copy2(self.bootanimation, './bootanimation_archive/system/media')
        copytree(f'./{file_type}/',
                 './bootanimation_archive/META-INF/com/google/android')
        r = int.from_bytes(urandom(19), 'big') >> (19 * 8 - 8)
        make_archive(f'{file_type}TWRP_BRP_{r}',
                     'zip',
                     './bootanimation_archive')
        rmtree('./Splash')
        rmtree('./Bootanimation')
        rmtree('./bootanimation_archive')
        self.del_temp()
        self.bootanimation = False
        showinfo(title='Succes', message=self.archive_maked)
        unpack_archive('resources.zip')

    def main_window(self):
        self.window = Tk()
        self.window.title('BRP PACKER | @Ulbandus')
        self.window.protocol('WM_DELETE_WINDOW', self.exit_of_programm)        
        self.type_of_archive = Combobox(self.window,
                                        values=['Bootanimation', 'Splash'],
                                        state="readonly")
        select_file_button = Button(
            self.window, text=self.select_file_text,
            background='black',
            fg='white',
            command=self.get_file)
        make_archive_button = Button(
            self.window,
            text=self.make_archive_text,
            background='black',
            fg='white',
            command=self.make_bootanimation_archive)
        self.type_of_archive.current(0)
        self.type_of_archive.grid(column=2, row=0)   
        select_file_button.grid(column=1, row=0)
        make_archive_button.grid(column=0, row=0)
        self.window.mainloop()

    def get_file(self):
        self.bootanimation = askopenfilename()
        if not self.bootanimation:
            return

    def exit_of_programm(self):
        self.del_temp()
        try:
            remove('./icon.ico')
            remove('./lang_pack.brp')
        except:
            pass        
        try:
            self.window.destroy()
        except:
            pass
        exit()

BRP_PACKER()
