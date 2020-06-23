from shutil import make_archive, copytree, copy2, rmtree
from tkinter.messagebox import showerror, showinfo, showwarning
from os.path import getsize, join
from os import walk, mkdir, rename
from tkinter import Tk, Button
from tkinter.filedialog import askopenfilename
from random import randrange as rr
from tkinter.ttk import Combobox

class BRP_PACKER:
    def __init__(self):
        self.del_temp()
        if not self.check_files():
            self.exit_of_programm()
        else:
            self.show_FAQ()
        self.bootanimation = False
        self.main_window()
        
    def del_temp(self):
        try:
            rmtree('./bootanimation_archive')
            rmtree('./temp')
        except:
            pass
        
    def make_bootanimation_archive(self):
        if not self.bootanimation:
            self.showmessage('ERROR', 'Файл не выбран', 'error')
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
        self.showmessage('Succes', 'Архив создан!', 'info')

    def pack(self):
        make_archive(f'{self.type_of_archive.get()}TWRP_BRP_{rr(1, 1000)}',
                     'zip',
                     './bootanimation_archive')

    def main_window(self):
        self.window = Tk()
        self.window.title('BRP PACKER | by @Ulbandus')
        self.window.geometry('304x27')
        self.window.tkraise()
        self.window.iconbitmap('icon.ico')
        self.window.grab_set()
        self.window.resizable(False, False)
        self.type_of_archive=Combobox(self.window,
                            values=['Bootanimation', 'Splash'],
            state="readonly")
        self.type_of_archive.current(1)
        self.type_of_archive.grid(column=2, row=0)
        self.select_file_button=Button(self.window, text='Выбрать файл',
                                        background='black',
                                        pady='2',
                                        width='12', fg='white',
                                        command=self.get_file)
        self.select_file_button.grid(column=1, row=0)
        self.select_file_button = Button(self.window, text='Создать архив',
                                        background='black',
                                        pady='2',
                                        width='12',
                                        fg='white',
                                        command=self.make_bootanimation_archive)
        self.select_file_button.grid(column=0, row=0)
        self.window.mainloop()

    def get_file(self):
        window = Tk().withdraw()
        self.bootanimation = askopenfilename()
        mkdir('./temp/')
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
            'Разработчик: Ulbandus\nЯзык: Python3\n4pda: https://4pda.ru/f' +
            'orum/index.php?showuser=8298432', 'info')

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
                message='Произошла неизвестная ошибка\nПрограмма паталась' +
                f' вывести\n{title}\n{message}\n Сообщите разработчику об этом')
            
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
                'Директория Recourses повреждена, что-то может пойти не так',
                'warning')
            return False
        if not self.get_size('./updaters/') == 724972:
            self.showmessage(
                'Updaters ERROR',
                'Директория Updaters повреждена, что-то может пойти не так',
                'warning')
            return False
        return True

    def exit_of_programm(self):
        try:
            self.window.destroy()
        except:
            pass
        exit()

BRP_PACKER()
