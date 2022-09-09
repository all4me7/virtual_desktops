import os
from time import sleep

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import keyboard
import pygetwindow
from pygame import mixer
from pyvda import AppView as view
from pyvda import VirtualDesktop as desktop
from pyvda import get_virtual_desktops

DESCRIPTION: str = f"""
VIRTUAL-DESKTOPS
----------------
CTRL + ALT: Switch beetwen 2 desktops
CTRL + WIN + ALT: Move active window to next desktop
SHIFT + ALT: Minimize/Maximize active window
"""

mixer.init()
desktop.create() if len(get_virtual_desktops()) == 1 else ...


class DataContainer:
    FIRST_DESKTOP: int = 1
    SECOND_DESKTOP: int = 2
    SWITCH_DESKTOP_SOUND: str = "./static/output.mp3"
    REVERSED_SWITCH_DESKTOP_SOUND: str = "./static/reversed_output.mp3"
    ACTIVATION_HOTKEY_1: str = "ctrl+alt"
    ACTIVATION_HOTKEY_2: str = "ctrl+win+alt"
    ACTIVATION_HOTKEY_3: str = "shift+alt"
    TIME_VALUE: float = 0.7
    VOLUME_LEVEL: float = 0.1


def playsound(file: str) -> None:
    mixer.music.load(file)
    mixer.music.play()
    mixer.music.set_volume(DataContainer.VOLUME_LEVEL)
    sleep(DataContainer.TIME_VALUE)
    mixer.music.stop()


def move_window() -> None:
    current_desktop: int = desktop.current().number
    window: object = view.current()

    if current_desktop == DataContainer.FIRST_DESKTOP:
        window.move(desktop(DataContainer.SECOND_DESKTOP))
        sleep(DataContainer.TIME_VALUE)
    else:
        window.move(desktop(DataContainer.FIRST_DESKTOP))
        sleep(DataContainer.TIME_VALUE)


def desktop_switch() -> None:
    current_desktop: int = desktop.current().number

    if current_desktop == DataContainer.FIRST_DESKTOP:
        desktop(DataContainer.SECOND_DESKTOP).go()
        playsound(DataContainer.SWITCH_DESKTOP_SOUND)
    else:
        desktop(DataContainer.FIRST_DESKTOP).go()
        playsound(DataContainer.REVERSED_SWITCH_DESKTOP_SOUND)


def minimize_window() -> None:
    current_window = pygetwindow.getActiveWindow()

    if current_window.isMinimized:
        current_window.restore()
        sleep(DataContainer.TIME_VALUE)
    else:
        current_window.minimize()
        sleep(DataContainer.TIME_VALUE)


def run():
    os.system("cls")
    print(DESCRIPTION.strip())
    keyboard.add_hotkey(DataContainer.ACTIVATION_HOTKEY_1, desktop_switch)
    keyboard.add_hotkey(DataContainer.ACTIVATION_HOTKEY_2, move_window)
    keyboard.add_hotkey(DataContainer.ACTIVATION_HOTKEY_3, minimize_window)
    keyboard.wait()


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        os._exit(1)
