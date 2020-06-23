from shutil import make_archive, copytree, copy2, rmtree, unpack_archive
from tkinter.messagebox import showerror, showinfo, showwarning
from os.path import getsize, join
from os import walk, mkdir, rename, rmdir
from tkinter import Tk, Button
from tkinter.filedialog import askopenfilename
from random import randrange as rr
from tkinter.ttk import Combobox
from locale import getdefaultlocale
from time import sleep

class BRP_PACKER:
    def __init__(self):
        self.del_temp()
        self.make_lang()
        unpack_archive('resources.zip')
        unpack_archive('./updaters.zip')
        if not self.check_files():
            self.exit_of_programm()
        self.show_FAQ()
        unpack_archive('./programm_resources.zip')
        self.bootanimation = False
        self.main_window()

    def make_lang(self):
        locale_str = getdefaultlocale()[0]
        if 'ru' in locale_str:
            lang = 'ru'
        elif 'eo' in locale_str:
            lang = 'esperanto'
        elif 'ja' in locale_str:
            lang = 'japanese'
        else:
            lang = 'english'
        if lang == 'ru':
            self.file_dont_selected = 'Файл не выбран'
            self.archive_maked = 'Архив создан!'
            self.icon_ico_warning = 'Файл icon.ico не найден'
            self.select_file_text = 'Выбрать файл'
            self.make_archive_text = 'Создать архив'
            self.developer_text = 'Разработчик'
            self.lang_text = 'Язык'
            self.resources_error_message = 'Директория Recourses повре' +\
                'ждена, что-то может пойти не так'
            self.updaters_error_message = 'Директория Updaters поврежден' +\
                'а, что-то может пойти не так'
        elif lang == 'esperanto':
            self.file_dont_selected = 'Neniu dosiero elektita'
            self.archive_maked = 'Arkivo kreita!'
            self.icon_ico_warning = 'Dosiero ikono.ico ne trovita'
            self.select_file_text = 'Elektu dosieron'
            self.make_archive_text = 'Krei arkivon'
            self.developer_text = 'Ellaboranto'
            self.lang_text = 'Lingvo'
            self.resources_error_message = 'Dosierujo pri Resursoj estas ' +\
                'difektita, io eble malaperos'
            self.updaters_error_message = 'Dosierujo pri Aktualigiloj korup' +\
                'tas, ke io povus malbone funkcii'
        elif lang == 'japanese':
            self.file_dont_selected = 'ファイルが選択されていません'
            self.archive_maked = 'アーカイブが作成されました！'
            self.icon_ico_warning = 'ファイルicon.icoが見つかりません'
            self.select_file_text = 'ファイルを選択'
            self.make_archive_text = 'アーカイブを作成する'
            self.developer_text = '開発者'
            self.lang_text = '言語'
            self.resources_error_message = 'リコースディレクトリが破損している' +\
                'ため、問題が発生する可能性があります'
            self.updaters_error_message = 'アップデータディレクトリが壊れているた' +\
                'め、問題が発生する可能性があります'
        else:
            self.file_dont_selected = 'No file selected'
            self.archive_maked = 'Archive created!'
            self.icon_ico_warning = 'File icon.ico not found'
            self.select_file_text = 'Select File'
            self.make_archive_text = 'Create archive'
            self.developer_text = 'Developer'
            self.lang_text = 'Language'
            self.resources_error_message = 'Recourses directory is damage' +\
                'd, something may go wrong'
            self.updaters_error_message = 'Updaters directory is corrupt' +\
                'something might go wrong'

    def del_temp(self):
        try:
            rmdir('./programm_resources.zip')
        except:
            pass
        try:
            rmdir('./updaters.zip')
        except:
            pass
        try:
            rmtree('./bootanimation_archive')
        except:
            pass
        try:
            rmtree('./temp')
        except:
            pass
        try:
            rmtree('./programm_resources')
        except:
            pass
        try:
            rmtree('./updaters')
        except:
            pass

    def make_bootanimation_archive(self):
        if not self.bootanimation:
            self.showmessage('ERROR', self.file_dont_selected, 'error')
            return
        copytree('./programm_resources/', './bootanimation_archive/')
        if self.type_of_archive.get() == 'Splash':
            copy2(self.bootanimation, './bootanimation_archive/')
        else:
            copy2(self.bootanimation, './bootanimation_archive/system/media/')
        copytree(f'./updaters/{self.type_of_archive.get().strip()}/',
                 './bootanimation_archive/META-INF/com/google/android/')
        self.pack()
        self.del_temp()
        self.showmessage('Succes', self.archive_maked, 'info')

    def pack(self):
        make_archive(f'{self.type_of_archive.get()}TWRP_BRP_{rr(1, 1000)}',
                     'zip',
                     './bootanimation_archive')

    def main_window(self):
        self.window = Tk()
        self.window.protocol('WM_DELETE_WINDOW', self.exit_of_programm)
        self.window.title('BRP PACKER | by @Ulbandus')
        self.window.geometry('304x27')
        self.window.tkraise()
        try:
            self.window.iconbitmap('icon.ico')
        except:
            showerror("Warning!!!", self.icon_ico_warning, 'warning')
        self.window.grab_set()
        self.window.resizable(False, False)
        self.type_of_archive = Combobox(self.window,
                                        values=['Bootanimation', 'Splash'],
                                        state="readonly")
        self.type_of_archive.current(1)
        self.type_of_archive.grid(column=2, row=0)
        self.select_file_button = Button(
            self.window, text=self.select_file_text,
            background='black',
            pady='2',
            width='12', fg='white',
            command=self.get_file)
        self.select_file_button.grid(column=1, row=0)
        self.select_file_button = Button(
            self.window,
            text=self.make_archive_text,
            background='black',
            pady='2',
            width='12',
            fg='white',
            command=self.make_bootanimation_archive)
        self.select_file_button.grid(column=0, row=0)
        self.window.mainloop()

    def get_file(self):
        window = Tk().withdraw()
        self.window.iconify()
        self.bootanimation = askopenfilename()
        self.window.deiconify()
        mkdir('./temp')
        copy2(self.bootanimation, './temp/')
        self.bootanimation_temp = self.bootanimation.split('/')[-1]
        if self.type_of_archive.get() == 'Splash':
            rename('./temp/' + self.bootanimation_temp, './temp/Splash.img')
            self.bootanimation = './temp/Splash.img'
        else:
            rename('./temp/' + self.bootanimation_temp,
                   './temp/bootanimation.zip')
            self.bootanimation = './temp/bootanimation.zip'

    def show_FAQ(self):
        self.showmessage(
            'ABOUT',
            f'{self.developer_text}: Ulbandus\n{self.lang_text}: Python3',
            'info')

    def showmessage(self, title, message, msg_type):
        window = Tk()
        window.withdraw()
        if msg_type == 'error':
            showerror(title=title, message=message)
        elif msg_type == 'info':
            showinfo(title=title, message=message)
        elif msg_type == 'warning':
            showwarning(title=title, message=message)
        else:
            showerror(
                title='UNKOWN ERROR',
                message=f'{message}, {title}, -|- ERROR')

    def get_size(self, directory):
        total_size = 0
        for dirpath, dirnames, filenames in walk(directory):
            for file in filenames:
                filepath = join(dirpath, file)
                total_size += getsize(filepath)
        return total_size

    def check_files(self):
        if not self.get_size('./resources/') == 0:
            self.showmessage(
                'Recourses ERROR',
                self.resources_error_message,
                'warning')
            return False
        if not self.get_size('./updaters/') == 724972:
            self.showmessage(
                'Updaters ERROR',
                self.updaters_error_message,
                'warning')
            return False
        return True

    def exit_of_programm(self):
        self.window.iconify()
        sleep(0.3)
        try:
            self.del_temp()
        except:
            pass        
        try:
            self.window.destroy()
            self.window.quit()
        except:
            pass
        exit()


BRP_PACKER()
