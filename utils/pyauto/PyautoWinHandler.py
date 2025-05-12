import logging
import os
import time

import pyautogui

log = logging
# yauto


class PyautoWinHandler:

    def __init__(self):
        pass

    def pyauto_uploadFile(self, filePath, key):
        """
            Method to handle to Window popup using pyauto
        """
        log.info("Method to select the file from window popup")
        time.sleep(2)
        pyautogui.getActiveWindow()
        pyautogui.write(os.getcwd() + filePath)
        pyautogui.press(key)
