import pyautogui


class Mouse:
    """
    A class to encapsulate mouse control actions using the pyautogui library.
    Includes movement, clicking, and additional utility methods for better usability.
    """
    def __init__(self):
        """
        Initializes the Mouse class. Ensures the pyautogui failsafe feature is enabled.
        """
        pyautogui.FAILSAFE = True  # Allow moving the mouse to the top-left corner to stop execution.

    def move(self, x: int, y: int, duration: float = 1.0):
        """
        Moves the mouse to a specific (x, y) position on the screen over a specified duration.

        :param x: The x-coordinate to move to.
        :param y: The y-coordinate to move to.
        :param duration: The time (in seconds) it takes to complete the movement.
        """
        try:
            pyautogui.moveTo(x, y, duration=duration)
            print(f"Mouse moved to ({x}, {y}) over {duration} seconds.")
        except Exception as e:
            print(f"Error moving mouse: {e}")

    def click(self, x: int, y: int, duration: float = 1.0, button: str = 'left'):
        """
        Clicks the mouse at a specific (x, y) position on the screen with the specified button.

        :param x: The x-coordinate to click.
        :param y: The y-coordinate to click.
        :param duration: The time (in seconds) it takes to move and click.
        :param button: The mouse button to click ('left', 'right', 'middle').
        """
        try:
            pyautogui.click(x, y, duration=duration, button=button)
            print(f"Mouse clicked at ({x}, {y}) with {button} button over {duration} seconds.")
        except Exception as e:
            print(f"Error clicking mouse: {e}")

    def scroll(self, clicks: int):
        """
        Scrolls the mouse vertically.

        :param clicks: Number of clicks to scroll. Positive scrolls up, negative scrolls down.
        """
        try:
            pyautogui.scroll(clicks)
            print(f"Scrolled {clicks} clicks.")
        except Exception as e:
            print(f"Error scrolling: {e}")


