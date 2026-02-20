from load_dotenv import load_dotenv
load_dotenv()
from PIL import Image
import higgsfield_client

image_path = './_img/11fec533-7c6f-41c1-b871-ee32d82a23d0-imagen.png'


# Upload PIL image



image = Image.open(image_path)
url = higgsfield_client.upload_image(image, format='png')


print("Generating video from image...")
# Image-to-video using Higgsfield's DoP (Director of Photography) model
result = higgsfield_client.subscribe(
    './_img/11fec533-7c6f-41c1-b871-ee32d82a23d0-imagen.png',
    arguments={
        'model': 'dop-standard',           # or 'dop-standard' for better quality
        'prompt': 'Cinematic dolly shot, subject looks into the camera slowly',
        'input_images': [
            {
                'type': 'image_url',
                'image_url': 'https://example.com/your-image.jpg'  # your image URL
            }
        ]
    }
)
print("Video generation in progress...")
print("Video URL:", result['url'])