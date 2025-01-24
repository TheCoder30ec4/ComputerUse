import pyautogui

class ScreenShort:
    
    def __init__(self):
        pass 
    
    def screenshot(self):
        """
        Takes a screenshot of the entire screen and saves it to the current directory.
        """
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save("./ScreenShorts/screenshot.png")
            print("Screenshot saved as 'screenshot.png'")
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            
if __name__ == "__main__":
    screen = ScreenShort()
    screen.screenshot()