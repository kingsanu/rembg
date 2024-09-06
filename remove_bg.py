from rembg import remove
from PIL import Image
import io

# Load input image
input_path = '1.webp'  # Replace with your image path
output_path = 'output_image.png'  # Replace with the output path

# Open the input image
with open(input_path, 'rb') as img_file:
    input_image = img_file.read()

# Remove the background
output_image = remove(input_image)

# Save the output image
with open(output_path, 'wb') as out_file:
    out_file.write(output_image)

print(f"Background removed. Output saved at {output_path}")
