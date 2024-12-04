
import pyautogui
import time
import keyboard
import logging
import sys

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurações globais
BATTLE_REGION = (0, 0, 177, 201)
LOOT_REGION = (768, 361, 208, 208)

LOOT_IMG = 'C:/Users/JeffDev/Documents/projects/tibia-bot/imgs/loot_wasp.png'
EMPTY_BATTLE_IMG = 'C:/Users/JeffDev/Documents/projects/tibia-bot/imgs/empty_battle3.png'
ATTACKING_IMG = 'C:/Users/JeffDev/Documents/projects/tibia-bot/imgs/attacking6.png'
#LOOT_IMG = 'C:/Users/JeffDev/Documents/projects/tibia-bot/imgs/loot_area.png'
last_attack = time.time()
attack_cooldown = 5
running = True

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
        return pyautogui.locateOnScreen(ATTACKING_IMG, region=BATTLE_REGION, confidence=0.8)
    except:
        return None

def attack():
    """Ataca um monstro"""
    global last_attack  #global p poder modificar a variavel
    current_time = time.time()
    if current_time - last_attack >= attack_cooldown:
        pyautogui.press('space')
        last_attack = current_time
        logger.info("Atacando...")

def get_loot():
    try:
        loot_locations = pyautogui.locateAllOnScreen(LOOT_IMG, confidence=0.9)
        for location in loot_locations:
            x, y = pyautogui.center(location)
            pyautogui.moveTo(x, y, duration=0.2)
            pyautogui.click(button="right")
            logger.info("Loot coletado!")
            break
    except Exception:
        return None
        
def stop_bot():
    """Para o bot"""
    global running
    running = False
    logger.info("Encerrando bot...")

def run_bot():
    """Função principal do bot"""
    logger.info("Bot iniciado. Pressione 'h' para começar...")
    keyboard.wait('h')
    
    empty_count = 0

    keyboard.on_press_key('c', lambda _: stop_bot() if keyboard.is_pressed('ctrl') else None)
    
    while running:
        battle_empty = check_battle()
        get_loot()

        if not battle_empty:
            empty_count = 0
            is_attacking = check_attack()
            
            if not is_attacking:
                attack()
            
        else:
            empty_count += 1
            if empty_count >= 5:
                logger.info("Battle list vazia, aguardando monstros...")
                empty_count = 0
        
        time.sleep(0.2)

    logger.info("Bot finalizado com sucesso!")

# Inicia o bot
if __name__ == "__main__":
    try:
        run_bot()
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
    finally:
        sys.exit(0)