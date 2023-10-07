import os
import shutil
from pathlib import Path
from win32com.client import Dispatch
import os
import tkinter as tk
from tkinter import messagebox

def create_shortcut(target_path, shortcut_path, working_directory, icon_path=None, icon_index=0):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target_path
    shortcut.WorkingDirectory = working_directory
    if icon_path:
        shortcut.IconLocation = (icon_path, icon_index)
    shortcut.Save()

#E:/Project/LANGUAGE/Memrapdesktopapp/reviseorlearn
#E:/Project/LANGUAGE/Memrapdesktopapp/main

if __name__ == "__main__":
    file1 = r""f"{os.getcwd()}""\ROL.exe"
    file1=file1.replace("\\", "/")
    #print(file1)
    file2 = r""f"{os.getcwd()}""\Add.exe"
    file2 = file2.replace("\\", "/")
    #print(file2)
    #print(os.path.join(os.path.dirname(__file__)))
    shortcut_file1 = r""f"{os.getcwd()}""\ROL.lnk"
    shortcut_file1 = shortcut_file1.replace("\\", "/")
    print(shortcut_file1)
    shortcut_file2 = r""f"{os.getcwd()}""\MEMRAP.lnk"
    shortcut_file2 = shortcut_file2.replace("\\", "/")

    print(shortcut_file2)

    #print(working_dir)
    working_dir = r""f"{os.getcwd()}"""
    working_dir = working_dir.replace("\\", "/")
    print(working_dir)
    #icon_path = r"E:\Project\LANGUAGE\Memrapdesktopapp\revise.ico"
    #icon_index = 1
    startup_folder = Path(os.getenv("APPDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    #print(startup_folder)
    #startup_folder  = startup_folder.replace("\\", "/")
    desktop_folder = Path(os.path.expanduser("~/Desktop"))
    #print(desktop_folder)
    #desktop_folder = desktop_folder.replace("\\", "/")
    create_shortcut(file1, shortcut_file1, working_dir)
    create_shortcut(file2, shortcut_file2, working_dir)
    shortfile1 = Path("ROL.lnk")
    #shortfile1 = shortfile1.replace("\\", "/")
    shortfile2 = Path("MEMRAP.lnk")
    #shortfile2 = shortfile2.replace("\\", "/")
    #os.rename(old_file_path, new_file_name)
    try:
        shutil.move(shortfile1, startup_folder / shortfile1.name)
        shutil.move(shortfile2, desktop_folder / shortfile2.name)
        print("Win")
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("MEMRAP Thông báo ( ఠ ͟ʖ ఠ)", "✓ Đã Cài Đặt Thành Công Phần Mềm! ✓")
        root.destroy()
    except FileNotFoundError as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("MEMRAP Thông báo ( ఠ ͟ʖ ఠ)", "1✕ Thiết bị không phù hợp! ✕\nERROR:shortcut file")
        root.destroy()
    except shutil.Error as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("MEMRAP Thông báo ( ఠ ͟ʖ ఠ)", "2✕ Thiết bị không phù hợp! ✕\nERROR:moving")
        root.destroy()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("MEMRAP Thông báo ( ఠ ͟ʖ ఠ)", f"3✕ Thiết bị không phù hợp! ✕\nERROR:{e}")
        root.destroy()
