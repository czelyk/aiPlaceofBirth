import os
import requests
from dotenv import load_dotenv
from aiCountries import AICountries
import re
from coordinator import get_coordinates  # Importing the new function

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_CX")

# Initialize the AI Countries class
ai_countries = AICountries()

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

        # Get coordinates for the city using the new function
        coordinates = get_coordinates(location)
        if coordinates:
            lat, lon = coordinates
            # Define the filename and save path with coordinates
            file_name = os.path.join(
                os.getcwd(), "pictures", f"{query.replace(' ', '_')}!3d{lat}!4d{lon}!.jpg"
            )

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
            match = re.search(r"Celebrity: (.+?) \(born in (.+?)\)", entry)
            if match:
                celebrity_name = match.group(1).strip()
                birth_city = match.group(2).strip()
                print(f"{celebrity_name} from {birth_city}")
                get_first_image(celebrity_name, birth_city)
            else:
                print(f"Skipping invalid entry: {entry}")
        except Exception as e:
            print(f"Error processing entry '{entry}': {e}")
