import Gemini
import Mouse
import Keyboard
import ScreenShort
import json
import pyautogui
import time


def initialization():
    """
    Initialize the required classes for the automation process.
    """
    # Initialize the Gemini API
    screen_size = pyautogui.size()
    gemini = Gemini.CallGemini(
        api_key="AIzaSyBK1OrJEbtVmQ39y28_FDhNgHiQMiCaApU", 
        prompt=""
    )
    print("Gemini API initialized.")

    # Initialize the Mouse controller
    mouse = Mouse.Mouse()
    print("Mouse controller initialized.")

    # Initialize the Keyboard controller
    keyboard = Keyboard.keyboard()
    print("Keyboard controller initialized.")

    # Initialize the ScreenShort controller
    screen = ScreenShort.ScreenShort()
    print("ScreenShort controller initialized.")

    return gemini, mouse, keyboard, screen, screen_size


def generate_prompt(screen_size, previous_action):
    """
    Generate the dynamic prompt for Gemini API with the previous action.
    """
    return f"""
    You are an Investor Relations Manager at a company. Your objective is to collect all email addresses 
    associated with a given company name by interacting with a computer interface of screen size {screen_size.width}x{screen_size.height}. 
    The previous action performed was: {previous_action}

    Instructions:
    1. Analyze the screenshot provided to identify actionable areas for interaction.
    2. Return a single JSON object for the next action in the format:
       {{
           "action": "click",
           "coordinates": [120, 45]
       }}
    3. Ensure the JSON object corresponds to only one action at a time.
    4. The `action` can be one of the following:
        - "click" with "coordinates" [x, y].
        - "move" with "coordinates" [x, y].
        - "scroll" with "coordinates" [dx, dy].
        - "type" with "text" as the input to type.
    5. Maintain precision in identifying actionable coordinates. Assume coordinates start at [0,0].

    Requirements:
    - Do not include additional text or explanations in your output.
    - Always output only one JSON object for each interaction.
    """


def save_json(input_string: str) -> dict:
    """
    Extract and parse JSON data from the input string.
    """
    try:
        clean_input_string = input_string[input_string.find('{'):input_string.rfind('}') + 1]
        json_data = json.loads(clean_input_string)
        print("Successfully processed the JSON data 🌟")
        return json_data
    except Exception as e:
        print(f"Error processing JSON: {e}")
        return {}


def main():
    gemini, mouse, keyboard, screen, screen_size = initialization()
    previous_action = "No previous action provided."

    while True:
        # Generate the dynamic prompt with the previous action
        prompt = generate_prompt(screen_size, previous_action)
        gemini.prompt = prompt

        # Step 1: Take a screenshot
        screen.screenshot()

        # Step 2: Get the action coordinates from the Gemini API
        response = gemini.generate_action_coordinates("./ScreenShorts/screenshot.png")
        print(response)
        response_json = save_json(response)

        if not response_json:
            print("No actionable response. Retrying...")
            continue

        # Update the previous action for the next iteration
        previous_action = json.dumps(response_json)

        # Step 3: Perform the action based on response
        if response_json['action'] == 'click':
            x, y = response_json["coordinates"]
            mouse.click(x=x, y=y)
        elif response_json['action'] == 'move':
            x, y = response_json["coordinates"]
            mouse.move(x=x, y=y)
        elif response_json['action'] == 'scroll':
            dx, dy = response_json["coordinates"]
            mouse.scroll(dx=dx, dy=dy)
        elif response_json['action'] == 'type':
            text = response_json['text']
            keyboard.type(text)
        elif response_json.get('text') == 'email':
            print("Email text detected. Exiting...")
            break  # Exit loop when 'email' text is found

        # Add a delay to avoid overwhelming the system
        time.sleep(10)


if __name__ == "__main__":
    main()
