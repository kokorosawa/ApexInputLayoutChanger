import pystray
from PIL import Image
from pystray import MenuItem
import threading
from controller import main, LayoutChanger
import sys
import threading
import os
import win32api
import win32con


class MyThread(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == "call":
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == "line":
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


def error_message():
    win32api.MessageBox(
        0, "Resolution not found", "Resolution not found", win32con.MB_OK
    )


def ChangerOn(icon, item):
    global Changertext, Changer, ChangerAction
    if Changertext == "ChangerOn" and LayoutChanger.get_setting():
        Changertext = "ChangerOff"
        Changer = MyThread(target=main, daemon=True)
        Changer.start()
    elif Changertext == "ChangerOff" and LayoutChanger.get_setting():
        Changertext = "ChangerOn"
        Changer.kill()
        icon.update_menu()
    else:
        threading.Thread(target=error_message).start()


def on_exit(icon, item):
    icon.stop()


if __name__ == "__main__":
    Changertext = "ChangerOn"
    menu = [
        MenuItem(lambda text: Changertext, action=ChangerOn),
        MenuItem(text="Exit", action=on_exit),
    ]
    image = Image.open(
        os.path.dirname(os.path.dirname(__file__)) + "\\static\\apex_icon.png"
    )
    icon = pystray.Icon("ApexInputLayoutChanger", image, "ApexInputLayoutChanger", menu)
    icon.run()
