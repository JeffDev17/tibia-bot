import cv2
import numpy as np
import pyautogui
import time
from constants import *
import actions
import json
import keyboard
import logging
from typing import Optional, Tuple

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_template(path: str) -> Optional[np.ndarray]:
    """Load and prepare an image template for matching."""
    try:
        template = cv2.imread(path)
        if template is None:
            logger.error(f"Erro ao carregar template: {path}")
            return None
        return cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        logger.error(f"Erro ao processar template: {str(e)}")
        return None

def find_on_screen(template_path: str, region: Tuple[int, int, int, int], threshold: float = 0.9) -> Optional[Tuple[int, int]]:
    """
    Find template image on screen using OpenCV.
    Returns center coordinates if found, None otherwise.
    """
    try:
        # Capture screen region
        screenshot = pyautogui.screenshot(region=region)
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        
        # Load and check template
        template = load_template(template_path)
        if template is None:
            return None
        
        # Perform template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            # Calculate center position
            template_h, template_w = template.shape
            center_x = max_loc[0] + template_w // 2 + region[0]
            center_y = max_loc[1] + template_h // 2 + region[1]
            return (center_x, center_y)
        
        return None
    except Exception as e:
        logger.error(f"Erro na detecção: {str(e)}")
        return None

def check_battle_status() -> bool:
    """
    Check battle status and handle combat.
    Continuously searches for and attacks monsters until none are found.
    Returns True if any attack was executed, False if no monsters were found.
    """
    MAX_EMPTY_CHECKS = 3  # Número de verificações vazias consecutivas para confirmar que não há mais monstros
    SCAN_DELAY = 3  # Delay entre verificações
    
    try:
        empty_checks = 0  # Contador de verificações sem encontrar monstros
        monster_found = False  # Flag para indicar se algum monstro foi encontrado durante todo o processo
        
        while empty_checks < MAX_EMPTY_CHECKS:
            # Verifica se há monstro no slot de batalha
            empty_battle = find_on_screen(EMPTY_BATTLE_IMG, BATTLE_REGION)
            
            if not empty_battle:  # Slot não está vazio (possível monstro presente)
                # Reseta o contador de verificações vazias já que encontramos algo
                empty_checks = 0
                
                # Inicia ataque
                logger.info("Monstro detectado - Iniciando ataque!")
                pyautogui.press('space')
                monster_found = True
                time.sleep(SCAN_DELAY)
                
            else:
                empty_checks += 1
                logger.debug(f"Nenhum monstro detectado (verificação vazia {empty_checks}/{MAX_EMPTY_CHECKS})")
                time.sleep(SCAN_DELAY)
        
        if monster_found:
            logger.info("Finalizado ciclo de ataques - Todos os monstros foram atacados")
        else:
            logger.info("Nenhum monstro encontrado na área")
            
        return monster_found
            
    except Exception as e:
        logger.error(f"Erro ao verificar status de batalha: {str(e)}")
        return False 

def go_to_flag(path, wait): 
    try: 
        flag = pyautogui.locateOnScreen(path, confidence=0.8, region=MAP_REGION) 
        
        if flag: x, y = pyautogui.center(flag) 
        pyautogui.moveTo(x, y) 
        pyautogui.click() 
        pyautogui.sleep(wait) 
       
    except: return None 
    
def check_player_position(): 
    try: pyautogui.locateOnScreen(PLAYER_IMG, confidence=0.8, region=MAP_REGION) 
    
    except: return None 

def try_loot():
    """Tenta pegar loot com tratamento de erro."""
    try:
        loot = pyautogui.locateOnScreen(LOOT_IMG, confidence=0.85)
        if loot:
            x, y = pyautogui.center(loot)
            pyautogui.moveTo(x, y)
            pyautogui.click(button='right')
            time.sleep(0.3)
    except Exception as e:
        logger.error("Loot nao encontrado")

def run_bot():
    """Main bot execution loop."""
    print("Bot está pronto! Pressione 'h' para iniciar...")
    keyboard.wait('h')
    
    try:
        with open(f'{FOLDER_NAME}/infos.json', 'r') as file:
            data = json.loads(file.read())
        
        while True:  # Loop principal
            for item in data:
                try:
                    # Execute combat sequence
                    if check_battle_status():
                        time.sleep(2)
                        try_loot()
                        actions.check_hunger()
                    
                    actions.check_status('Health', 1, *POSITION_HEALTH, COLOR_GREEN_HEALTH, 'F3')
                    time.sleep(1)
                    
                    actions.check_status('Mana', 5, *POSITION_MANA, COLOR_MANA, 'F3')
                    
                    # Navigation sequence
                    player_pos = check_player_position()
                    if player_pos is None:  # Player not found in current position
                        # We're at the flag, do actions here
                        check_battle_status()
                        time.sleep(0.5)
                        try_loot()
                        actions.hole_down(item['down_hole'])
                        actions.hole_up(item['up_hole'], f'{FOLDER_NAME}/anchor_floor2.png', 430, 0)
                        actions.hole_up(item['up_hole'], f'{FOLDER_NAME}/anchor_floor3.png', 130, 130)
                        # Move to next flag
                        go_to_flag(item['path'], item['wait'])
                    else:
                        # We're not at the flag yet, move to it
                        go_to_flag(item['path'], item['wait'])
                    
                    time.sleep(0.2)  # Pequeno delay entre iterações
                    
                except Exception as e:
                    logger.error(f"Erro durante execução do item: {str(e)}")
                    continue  # Continua para o próximo item mesmo se houver erro
                    
    except Exception as e:
        logger.error(f"Erro crítico durante a execução: {str(e)}")
        raise  # Re-raise o erro após logá-lo

if __name__ == "__main__":
    try:
        print("Iniciando bot em 3 segundos...")
        time.sleep(3)
        run_bot()
    except KeyboardInterrupt:
        print("\nBot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}")
        raise