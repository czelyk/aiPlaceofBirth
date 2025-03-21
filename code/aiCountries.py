import requests
import os
from dotenv import load_dotenv
import ollama
import re

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_CX")

# Initialize the AI Countries class
class AICountries:
    def __init__(self):
        self.model = ollama

    def get_random_countries(self):
        try:
            response = self.model.chat(model="llama2", messages=[{"role": "user", "content": "Generate the name of 10 countries randomly and one celebrity from them and which city they were born in."}])
            content = response['message']['content'] if 'message' in response and 'content' in response['message'] else ''
            countries = content.split("\n") if content else ["No countries generated"]
            return [country.strip() for country in countries if country.strip()]
        except Exception as e:
            print(f"Error: {e}")
            return ["Error retrieving countries"]

# Initialize AI Countries
ai_countries = AICountries()

def get_coordinates(location):
    search_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location,
        "key": API_KEY
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    if "results" in data and len(data["results"]) > 0:
        lat = data["results"][0]["geometry"]["location"]["lat"]
        lng = data["results"][0]["geometry"]["location"]["lng"]
        return lat, lng
    else:
        print(f"Could not find coordinates for {location}")
        return None


def get_first_image(query, location):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query + " portrait",
        "cx": CX,
        "key": API_KEY,
        "searchType": "image",
        "num": 1
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    if "items" in data:
        image_url = data["items"][0]["link"]
        print(f"Downloading image of {query} from: {image_url}")

        # Get the image content
        img_data = requests.get(image_url).content

        # Define the path to save the image in the 'pictures' folder
        pictures_folder = os.path.join(os.getcwd(), "pictures")
        if not os.path.exists(pictures_folder):
            os.makedirs(pictures_folder)  # Create the folder if it doesn't exist

        # Get coordinates for the location
        coordinates = get_coordinates(location)
        if coordinates:
            lat, lng = coordinates
            # Define the filename and save path (use the celebrity's name and city for naming)
            file_name = os.path.join(pictures_folder, f"{query.replace(' ', '')}!3d{lat}!4d{lng}!.jpg")

            # Save the image
            with open(file_name, 'wb') as f:
                f.write(img_data)
            print(f"Image saved as {file_name}\n")
    else:
        print(f"No image found for {query}.")


if __name__ == "__main__":
    print("Generating random countries and celebrities...")

    random_countries = ai_countries.get_random_countries()

    print("\nRaw AI Output:")
    print(random_countries)  # Debugging output

    print("\nGenerated Celebrities:")
    for entry in random_countries:
        print(f"Processing entry: {entry}")  # Debugging output
        try:
            # Try matching celebrity and birthplace
            match = re.search(r"Celebrity: (.+?)\s*Born in\s*(.+)", entry)
            if match:
                celebrity_name = match.group(1).strip()
                birth_city = match.group(2).strip()
                print(f"{celebrity_name} from {birth_city}")
                get_first_image(celebrity_name, birth_city)
            else:
                # Try matching in a more general format
                match = re.search(r"Celebrity: (.+?)\s*Birthplace: (.+)", entry)
                if match:
                    celebrity_name = match.group(1).strip()
                    birth_city = match.group(2).strip()
                    print(f"{celebrity_name} from {birth_city}")
                    get_first_image(celebrity_name, birth_city)
                else:
                    print(f"Skipping invalid entry: {entry}")
        except Exception as e:
            print(f"Error processing entry '{entry}': {e}")
