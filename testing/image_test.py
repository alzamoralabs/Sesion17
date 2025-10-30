import openai
from dotenv import load_dotenv
load_dotenv()

image_size = "1024x1024" # Other options: "1024x1792", "1792x1024"
image_quality = "hd" # Other option: "standard"
number_of_images = 1

response = openai.images.generate(
    model="dall-e-3",  # Specify the DALL-E model (e.g., "dall-e-2" or "dall-e-3")
    prompt="A futuristic city skyline at sunset with flying cars and towering skyscrapers.",
    n=1,  # Number of images to generate
    size="1024x1024",  # Image size (e.g., "256x256", "512x512", "1024x1024")
    quality="standard" # Or "hd" for higher quality images
)
print(response)
image_url = response.data[0].url
print(f"Generated image URL: {image_url}")

# You can then download the image using a library like requests
import requests
image_data = requests.get(image_url).content
with open("generated_image.png", "wb") as f:
    f.write(image_data)
print("Image saved as generated_image.png")