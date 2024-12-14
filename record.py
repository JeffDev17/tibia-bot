import pyautogui as pg
from pynput.keyboard import Listener
from pynput import keyboard
import json
import os
import constants

def create_folder():
    if not os.path.isdir(constants.FOLDER_NAME):
        os.mkdir(constants.FOLDER_NAME)

class Rec:
    def __init__(self):
        create_folder()
        self.count = 0
        self.coordionates = []
    
    def photo(self):
        x, y = pg.position()
        photo = pg.screenshot(region=(x - 3, y - 3, 6, 6))
        path = f'{constants.FOLDER_NAME}/flag_{self.count}.png'
        photo.save(path)
        self.count = self.count + 1
        info = {
            "path": path,
            "down_hole": 0,
            "up_hole": 0,
            "wait": 10,
        }
        self.coordionates.append(info)

    def key_code(self, key):
        if key == keyboard.Key.esc:
            with open(f'{constants.FOLDER_NAME}/infos.json', 'w') as file:
                file.write(json.dumps(self.coordionates))
            return False
        if key == keyboard.Key.insert:
            self.photo()
        
        if key == keyboard.Key.page_up:
            self.up_hole()
        if key == keyboard.Key.page_down:
            self.down_hole()

    def down_hole(self):
        if self.coordionates:
            last_coordinates = self.coordionates[-1]
            last_coordinates["down_hole"] = 1

    def up_hole(self):
        if self.coordionates:
            last_coordinates = self.coordionates[-1]
            last_coordinates["up_hole"] = 1

    def start(self):
        with Listener(on_press=self.key_code) as listener:
            listener.join()

if __name__ == '__main__':
    record = Rec()
    record.start()