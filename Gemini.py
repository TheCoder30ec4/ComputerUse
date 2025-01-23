import base64
import google.generativeai as genai
import traceback


class CallGemini:
    """
    A class to interact with the Gemini Generative AI API for generating actionable coordinates 
    from an image based on a given prompt.
    """

    def __init__(self, api_key: str, prompt: str):
        """
        Initializes the CallGemini class with an API key and a user-defined prompt.

        :param api_key: API key for Gemini Generative AI.
        :param prompt: The instruction prompt to guide the AI model.
        """
        self.api_key = api_key
        self.prompt = prompt

        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model_name='gemini-1.5-pro')
            print("API configured successfully.")
        except Exception as e:
            print(f"Error configuring API: {e}")
            traceback.print_exc()
            raise

    @staticmethod
    def encode_image_to_base64(image_path: str) -> str:
        """
        Encodes an image to Base64 format.

        :param image_path: Path to the image file.
        :return: Base64-encoded string of the image.
        :raises FileNotFoundError: If the image file does not exist.
        """
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except FileNotFoundError:
            print(f"Error: File not found at {image_path}")
            raise

    def generate_action_coordinates(self, image_path: str) -> str:
        """
        Generates actionable coordinates by sending the image and prompt to the Gemini API.

        :param image_path: Path to the image file.
        :return: JSON string containing action coordinates, or None if an error occurs.
        """
        try:
            # Encode image to Base64
            encoded_image = self.encode_image_to_base64(image_path)

            # Prepare payload
            payload = [
                {"mime_type": "image/png", "data": encoded_image},
                {"text": self.prompt}
            ]

            # Call the Gemini API
            response = self.model.generate_content(payload)  # Verify this method with Gemini's API docs

            # Validate and process the response
            if response and hasattr(response, "candidates") and response.candidates:
                for candidate in response.candidates:
                    #print("Generated Response:", candidate.content.parts[0].text)
                    return candidate.content.parts[0].text

            print("No valid candidates found in the response.")
            return None

        except FileNotFoundError:
            print(f"Image file not found: {image_path}")
        except Exception as e:
            print(f"Error during content generation: {e}")
            traceback.print_exc()
        return None


# Example Usage
if __name__ == "__main__":
    # Example API key and prompt
    api_key = "AIzaSyBK1OrJEbtVmQ39y28_FDhNgHiQMiCaApU"
    previous_action = ""
    prompt = f"""
    You are an Investor Relations Manager at a company. Your objective is to collect all email addresses 
    associated with a given company name by interacting with a computer interface. You will be provided with a 
    screenshot of the computer screen and the previous action performed. {previous_action}

    Instructions:
    Analyze the screenshot to identify actionable areas for interaction.
    Provide a single JSON object for each action, formatted as follows:
    {
        "action": "click",
        "coordinates": [120, 45]
    }
    Requirements:
    Provide only the JSON object as output, with no additional text or explanation.
    Ensure each JSON object corresponds to only one single action.
    Maintain precision and accuracy in identifying actionable coordinates.
    """

    # Initialize the class and generate action coordinates
    gemini = CallGemini(api_key, prompt)
    image_path = "Screenshot.png"  # Replace with the actual path to your image
    result = gemini.generate_action_coordinates(image_path)

    if result:
        print("Action Coordinates:", result)
    else:
        print("Failed to generate action coordinates.")
