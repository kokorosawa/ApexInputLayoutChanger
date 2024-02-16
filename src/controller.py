from win32con import WM_INPUTLANGCHANGEREQUEST
import win32gui
import win32api
import win32con
import yaml
import time
import os

ENG_HEX = 0x4090409
ZHTW_HEX = 0x4040404


class LayoutChanger:
    def __init__(self):
        self.data = {}
        self.full_screen_rect = None

    def get_setting(self):
        try:
            with open(os.path.dirname(__file__) + "\\settings.yaml", "r") as stream:
                self.data = yaml.load(stream, Loader=yaml.CLoader)
                if (
                    self.data["Resolution"]["width"] != None
                    and self.data["Resolution"]["height"] != None
                ):
                    self.full_screen_rect = (
                        self.data["Resolution"]["width"],
                        self.data["Resolution"]["height"],
                    )
                    return True
                return False
        except Exception as e:
            print(e)

    def get_window_placement(self):
        window = win32gui.FindWindow("Respawn001", "Apex Legends")
        rect = win32gui.GetWindowRect(window)[2:]
        if rect == self.full_screen_rect:
            return True
        return False

    def change_input_language(self, HEX):
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        im_list = win32api.GetKeyboardLayoutList()
        im_list = list(map(hex, im_list))
        res = win32api.SendMessage(hwnd, WM_INPUTLANGCHANGEREQUEST, 0, HEX)
        if res == 0:
            if HEX == ENG_HEX:
                return ENG_HEX
            else:
                return ZHTW_HEX

    def check_apex_active(self):
        window = win32gui.FindWindow("Respawn001", "Apex Legends")
        if window != 0:
            return True
        return False


LayoutChanger = LayoutChanger()


def main():
    if LayoutChanger.get_setting():
        while LayoutChanger.check_apex_active():
            if LayoutChanger.get_window_placement():
                LayoutChanger.change_input_language(ENG_HEX)
            else:
                LayoutChanger.change_input_language(ZHTW_HEX)
            time.sleep(1)
        LayoutChanger.change_input_language(ZHTW_HEX)
    else:
        return False
