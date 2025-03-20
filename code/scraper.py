import os
import requests
from dotenv import load_dotenv
from aiLocation import AILocation

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_CX")

# Initialize the AI Location class
ai_location = AILocation()


def get_first_image(query):
    # Use AI model to get the location of the person
    location = ai_location.get_location_from_name(query)
    print(f"Location for {query}: {location}")

    # Now, search for the image based on the query
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": CX,
        "key": API_KEY,
        "searchType": "image",
        "num": 1
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    if "items" in data:
        image_url = data["items"][0]["link"]
        print("Downloading image from:", image_url)

        # Get the image content
        img_data = requests.get(image_url).content

        # Define the path to save the image in the 'pictures' folder
        pictures_folder = os.path.join(os.getcwd(), "pictures")
        if not os.path.exists(pictures_folder):
            os.makedirs(pictures_folder)  # Create the folder if it doesn't exist

        # Define the filename and save path (use the location for naming)
        file_name = os.path.join(pictures_folder, f"{query}_{location}.jpg")

        # Save the image
        with open(file_name, 'wb') as f:
            f.write(img_data)
        print(f"Image saved as {file_name}")
    else:
        print("No image found.")


# Example usage
if __name__ == "__main__":
    name = input("Enter a name: ")
    get_first_image(name)
