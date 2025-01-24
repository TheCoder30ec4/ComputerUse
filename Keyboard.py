import pyautogui
import time
class keyboard:
    
    def __init__(self):
        pass 
    def type(self, text: str):
        """
        Types the specified text at the current mouse position.

        :param text: The text to type.
        """
        try:
            time.sleep(2)
            pyautogui.typewrite(text)
            
            print(f"Typed: {text}")
        except Exception as e:
            print(f"Error typing text: {e}")
            
