import colorama
import json
import time
import threading
import keyboard
import sys
import os
import win32api
import pystyle
import time
from pystyle import Box, Center, Write, Colors, Colorate, Add
from ctypes import WinDLL
import numpy as np
from mss import mss as mss_module
from colorama import Fore, init
import ctypes
import random
import asyncio
import string
init(autoreset=True)
os.system('cls' if os.name == 'nt' else 'clear')
SUCCESS = "\x1b[38;5;255m[\x1b[32m+\x1b[38;5;255m]"
taikhoan = """Logged in as \033[1;31m""" + keyauthapp.user_data.username + """\033[1;39m."""
whxyu = """

                                   ______     _                       ____        __ 
                                 /_  __/____(_)___ _____ ____  _____/ __ )____  / /_
                                  / / / ___/ / __ `/ __ `/ _ \/ ___/ __  / __ \/ __/
                                 / / / /  / / /_/ / /_/ /  __/ /  / /_/ / /_/ / /_  
                                /_/ /_/  /_/\__, /\__, /\___/_/  /_____/\____/\__/  
                                           /____//____/                                           

                                     This is a free product of MCC's Archive.
                           Any attempt to exploit MCC Loader is a violation of the TOS.              
 """
print(taikhoan)
print(Colorate.Horizontal(Colors.red_to_white, whxyu, 1))
print(f"{SUCCESS} \033[1;32mF10 \033[1;39mto enable trigger bot")
print(f"{SUCCESS} \033[1;32mK \033[1;39mmust be Fire primary bind in \033[1;31mValorant")
print(f"{SUCCESS} Enemies color must be \033[1;35mPurple")
print(f"{SUCCESS} HotKey: \033[1;32mLAlt")
print(f"{SUCCESS} Trigger delays: \033[0;31mMax\033[1;39m(\033[0;31m10 \033[1;39mms)")


def exiting():
    try:
        exec(type((lambda: 0).__code__)(0, 0, 0, 0, 0, 0, b'\x053', (), (), (), '', '', 0, b''))
    except:
        try:
            sys.exit()
        except:
            raise SystemExit


user32, kernel32, shcore = (
    WinDLL("user32", use_last_error=True),
    WinDLL("kernel32", use_last_error=True),
    WinDLL("shcore", use_last_error=True),
)

shcore.SetProcessDpiAwareness(2)
WIDTH, HEIGHT = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

ZONE = 5
GRAB_ZONE = (
    int(WIDTH / 2 - ZONE),
    int(HEIGHT / 2 - ZONE),
    int(WIDTH / 2 + ZONE),
    int(HEIGHT / 2 + ZONE),
)


class triggerbot:
    def __init__(self):
        self.sct = mss_module()
        self.triggerbot = False
        self.triggerbot_toggle = True
        self.exit_program = False
        self.toggle_lock = threading.Lock()

        # Configuration
        self.config = {
            "trigger_hotkey": "0xA4",  # LAlt key
            "base_delay": 0.01,
            "trigger_delay": 10,
            "color_tolerance": 70,
            "always_enabled": False
        }

        try:
            self.trigger_hotkey = int(self.config["trigger_hotkey"], 16)
            self.always_enabled = self.config["always_enabled"]
            self.trigger_delay = self.config["trigger_delay"]
            self.base_delay = self.config["base_delay"]
            self.color_tolerance = self.config["color_tolerance"]
            self.R, self.G, self.B = (250, 100, 250)  # purple
        except:
            exiting()

    def cooldown(self):
        time.sleep(0.1)
        with self.toggle_lock:
            self.triggerbot_toggle = True
            kernel32.Beep(440, 75), kernel32.Beep(700, 100) if self.triggerbot else kernel32.Beep(440, 75), kernel32.Beep(200, 100)

    def searcherino(self):
        start_time = time.time()
        img = np.array(self.sct.grab(GRAB_ZONE))

        pmap = np.array(img)
        pixels = pmap.reshape(-1, 4)
        color_mask = (
                (pixels[:, 0] > self.R - self.color_tolerance) & (pixels[:, 0] < self.R + self.color_tolerance) &
                (pixels[:, 1] > self.G - self.color_tolerance) & (pixels[:, 1] < self.G + self.color_tolerance) &
                (pixels[:, 2] > self.B - self.color_tolerance) & (pixels[:, 2] < self.B + self.color_tolerance)
        )
        matching_pixels = pixels[color_mask]

        if self.triggerbot and len(matching_pixels) > 0:
            delay_percentage = self.trigger_delay / 100.0

            actual_delay = self.base_delay + self.base_delay * delay_percentage

            time.sleep(actual_delay)
            keyboard.press_and_release('k')
            end_time = time.time()
            print(f"{SUCCESS} Fired in:", int((end_time - start_time) * 1000), "ms")
            asyncio.sleep(1)
            print("\033[F\033[K", end="", flush=True)

    def toggle(self):
        if keyboard.is_pressed("f10"):
            with self.toggle_lock:
                if self.triggerbot_toggle:
                    self.triggerbot = not self.triggerbot
                    print(self.triggerbot)
                    self.triggerbot_toggle = False
                    threading.Thread(target=self.cooldown).start()

            if keyboard.is_pressed("ctrl+shift+x"):  # Check for the kkkkk keybind
                self.exit_program = True
                exiting()

    def hold(self):
        while True:
            while win32api.GetAsyncKeyState(self.trigger_hotkey) < 0:
                self.triggerbot = True
                self.searcherino()
            else:
                time.sleep(0.1)
            if keyboard.is_pressed("ctrl+shift+x"):  # Check for the exit keybind
                self.exit_program = True
                exiting()

    def starterino(self):
        while not self.exit_program:  # Keep running until the exit_program flag is True
            if self.always_enabled == True:
                self.toggle()
                self.searcherino() if self.triggerbot else time.sleep(0.1)
            else:
                self.hold()

    def titlespoof(self):
        title = "Sản phẩm này là bản trả phí của Vũ Nguyễn(nguboiz). Mọi hành vi leak/share trigger bot sẽ bị ban vĩnh viến HWID khỏi hệ thống!"

        def generate_glitched_title(title):
            valid_characters = string.ascii_letters + string.digits + string.punctuation + ' '
            glitched_title = ''.join(random.choice(valid_characters) for _ in title)
            return glitched_title

        while True:
            glitched_title = generate_glitched_title(title)
            ctypes.windll.kernel32.SetConsoleTitleW(glitched_title)
            time.sleep(0.03)

bot_instance = triggerbot()
threading.Thread(target=bot_instance.starterino).start()
threading.Thread(target=bot_instance.titlespoof).start()
# 1e72e5b0dd7609bd9a0ee6272befe8eb147dfbb22a8cff2b431e085b01714925
# 017f82a410ce9af2b4e0ac9f8576c17d4c99ef0125d881918fad941eb1b87aff
# a72cf292dd3adc0ac60ee5dba15bafc5de8cacbbb5e2d9a1bf15fec07f5fe8b4
# efe010657f01cd82216af06f0644b088369a797c4eae054835523b207f5b1adf
