import pyautogui
import time
import random
import logging
from constants import *

logger = logging.getLogger(__name__)

def check_battle():
    """Verifica se tem monstros na battle list"""
    try:
        is_empty = pyautogui.locateOnScreen(EMPTY_BATTLE_IMG, region=BATTLE_REGION, confidence=0.9)
        return is_empty is not None
    except:
        return False

def check_attack():
    """Verifica se está atacando"""
    try:
        return pyautogui.locateOnScreen(ATTACKING_IMG, region=BATTLE_REGION, confidence=0.9)
    except:
        return None

def attack():
    """Ataca um monstro"""
    global last_attack  #global p poder modificar a variavel
    current_time = time.time()
    if current_time - last_attack >= attack_cooldown:
        pyautogui.press('space')
        last_attack = current_time
        logger.info("Attacking...")

def get_loot():
    try:
        loot_locations = list(pyautogui.locateAllOnScreen(LOOT_IMG, confidence=0.85))
        if loot_locations:
            for location in loot_locations:
                x, y = pyautogui.center(location)   
                pyautogui.moveTo(x, y, duration=0.2)
                pyautogui.click(button="right")
                time.sleep(0.3)  # Add small delay between looting
                break
        
    except Exception:
        logger.error(f"No loot found")
        return None
    
def check_hunger():
    try:
        hungry = pyautogui.locateOnScreen(HUNGER_IMG, region=HUNGER_REGION, confidence=0.8)
        if hungry:
            food_location = pyautogui.locateOnScreen(FOOD_IMG, region=BACKPACK_REGION, confidence=0.8)
            if food_location:
                x, y = pyautogui.center(food_location)
                pyautogui.moveTo(x, y, duration=0.2)
                pyautogui.click(button="right")
                pyautogui.moveTo(x, y - 100, duration=0.2)
    except:
        return None

def check_status(name, delay, x, y, rgb, button_name):
    print(f"Checking {name}...")
    pyautogui.sleep(delay) 
    if pyautogui.pixelMatchesColor(x, y, rgb):
        pyautogui.press(button_name)

def random_movement():
    key = random.choice(MOVEMENT_KEYS)
    hold_time = random.uniform(0.1, 0.5)
    pyautogui.keyDown(key)
    time.sleep(hold_time)
    pyautogui.keyUp(key)
    logger.info('Random movement executed!')

def hole_down(should_down):
    if should_down:
        try: 
            hole = pyautogui.locateOnScreen(HOLE_IMG, confidence=0.7)
            if hole:
                x, y = pyautogui.center(hole)
                pyautogui.moveTo(x, y)
                pyautogui.click(button='left')
                pyautogui.sleep(5)
        except:
            return None

def hole_up(should_up, anchor_img, plus_x, plus_y):
    if should_up:
        try:
            hole = pyautogui.locateOnScreen(anchor_img, confidence=0.7)
            if hole:
                x, y = pyautogui.center(hole)
                pyautogui.moveTo(x + plus_x, y + plus_y)
                pyautogui.press('F9')
                pyautogui.click(button='left')
        except:
            return None
        
def execute_attack():
    """
    Executa a sequência de combate usando as funções de verificação e ataque.
    Retorna True se executou um ataque, False caso contrário.
    """
    # Verifica se há monstros (is_empty is not None significa que a battle list está vazia)
    if not check_battle():
        # Verifica se já está atacando
        is_attacking = check_attack()
        
        # Se não estiver atacando, inicia um novo ataque
        if not is_attacking:
            attack()
            return True
            
    return None
