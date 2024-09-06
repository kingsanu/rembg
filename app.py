from flask import Flask, request, jsonify
from rembg import remove
from PIL import Image, ImageFilter
import base64
from io import BytesIO

app = Flask(__name__)

def apply_oil_paint_effect(image):
    # Apply an oil paint-like effect
    return image.filter(ImageFilter.ModeFilter(size=3))  # Example oil-paint effect

@app.route('/remove_background', methods=['POST'])
def remove_background():
    # Get the image data from the request
    data = request.json
    image_data = data.get('image')

    # Get the 'oil_paint' parameter from the query string
    oil_paint = request.args.get('oil_paint', 'false').lower() == 'true'

    if not image_data:
        return jsonify({'error': 'No image data provided'}), 400

    try:
        # Decode the base64 image
        image_bytes = base64.b64decode(image_data)
        
        # Load the image using PIL
        input_image = Image.open(BytesIO(image_bytes))

        # Remove the background
        output_image_data = remove(image_bytes)

        # Convert output bytes back to an image
        output_image = Image.open(BytesIO(output_image_data))

        # Apply oil paint effect if requested
        if oil_paint:
            output_image = apply_oil_paint_effect(output_image)
            print("Oil paint effect successfully applied to the image.")  # Log success

        # Convert the processed image to base64
        buffered = BytesIO()
        output_image.save(buffered, format="PNG")
        output_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return jsonify({'image': output_base64})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
