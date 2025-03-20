import ollama
import re


class AILocation:
    def __init__(self):
        # Initialize the Ollama model
        self.model = ollama

    def get_location_from_name(self, name):
        try:
            # Modify the question to complete the sentence with the person's name
            response = self.model.chat(model="llama2", messages=[
                {"role": "user", "content": f"Complete the sentence: The person {name} was born in the city of ..."}])

            # Extract the content from the response
            content = response['message']['content'] if 'message' in response and 'content' in response[
                'message'] else ''

            # Check if content exists and extract the location
            if content:
                # Search for the city name after "city of"
                location_match = re.search(r'the city of\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', content)

                if location_match:
                    location = location_match.group(1)  # Extract the city name
                else:
                    location = "Location not found"
            else:
                location = "Could not determine the location."

            return location
        except Exception as e:
            # In case of an error (e.g., API issue or network problem)
            print(f"Error: {e}")
            return "Error retrieving location"
