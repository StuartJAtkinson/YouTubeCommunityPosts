import os
import re
import requests
from bs4 import BeautifulSoup

def download_community_images(channel_id, output_folder="community_images"):
    """
    Download all images from the Community tab of a specified YouTube channel.

    Args:
        channel_id (str): The ID of the YouTube channel (e.g., UCxxxxx).
        output_folder (str): The folder to save downloaded images.
    """
    # Define the Community tab URL for the channel
    community_url = f"https://www.youtube.com/channel/{channel_id}/community"

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Fetch the Community page
    print(f"Fetching Community posts from {community_url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    response = requests.get(community_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all image elements in the Community posts
    image_tags = soup.find_all("img", {"src": re.compile(r"ytimg\.com")})

    # Download images
    print(f"Found {len(image_tags)} images. Starting download...")
    for index, img_tag in enumerate(image_tags):
        img_url = img_tag["src"]
        try:
            # Fetch the image content
            img_data = requests.get(img_url).content

            # Save the image locally
            img_filename = os.path.join(output_folder, f"image_{index + 1}.jpg")
            with open(img_filename, "wb") as img_file:
                img_file.write(img_data)

            print(f"Downloaded: {img_filename}")
        except Exception as e:
            print(f"Failed to download image from {img_url}. Error: {e}")

    print("Download completed.")

# Example usage
if __name__ == "__main__":
    # Replace this with the YouTube channel ID you want to scrape
    channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Example: Google Developers Channel
    download_community_images(channel_id)
