import ctypes


def punish_remove_wallpaper():
    ctypes.windll.user32.SystemParametersInfoW(20, 0, "C:\\Windows\\System32\\win32k\\wallpaper.jpg", 3)


# punish_remove_wallpaper()
