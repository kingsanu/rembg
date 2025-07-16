# Background Removal API

A simple FastAPI application that removes backgrounds from images using the rembg library.

## Features

- Remove backgrounds from images via API
- Returns transparent PNG images
- Optional upload to cloud storage
- CORS enabled for all origins

## Installation

### Local Development

1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python -m uvicorn main:app --reload
   ```

### Deployment on Linux VPS with PM2

1. Install Node.js and PM2:

   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt install -y nodejs
   sudo npm install -g pm2
   ```

2. Create a startup script (start_app.sh):

   ```bash
   #!/bin/bash
   cd /path/to/your/app
   source venv/bin/activate
   exec python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. Make it executable:

   ```bash
   chmod +x start_app.sh
   ```

4. Start with PM2:
   ```bash
   pm2 start ./start_app.sh --name "bg-remover"
   pm2 startup
   pm2 save
   ```

## API Usage

### Remove Background

**Endpoint:** `POST /remove-bg`

**Request:**

- Content-Type: multipart/form-data
- Body:
  - `file`: (required) Image file to remove background from
  - `upload`: (optional) Boolean flag to upload the result to cloud storage (default: false)
  - `user_id`: (optional) User ID for the uploaded image (default: "anonymous")
  - `filename`: (optional) Custom filename for the uploaded image (default: auto-generated UUID)

Note: The `upload`, `user_id`, and `filename` parameters can be provided either as form data or as URL query parameters. Form data takes precedence over query parameters.

**Response:**

When `upload=false` (default):

- Content-Type: image/png
- Body: Transparent PNG image

When `upload=true`:

- Content-Type: application/json
- Body: JSON object with the following properties:
  ```json
  {
    "url": "https://storage-url.com/image.png",
    "filename": "generated-filename.png",
    "userId": "user-id"
  }
  ```

### Example with cURL

```bash
# Download the image directly
curl -X POST -F "file=@your_image.jpg" http://localhost:8000/remove-bg -o output.png

# Upload to cloud storage using form data
curl -X POST -F "file=@your_image.jpg" -F "upload=true" -F "user_id=user123" -F "filename=my-image.png" http://localhost:8000/remove-bg

# Upload to cloud storage using URL query parameters
curl -X POST -F "file=@your_image.jpg" "http://localhost:8000/remove-bg?upload=true&user_id=user123&filename=my-image.png"
```

### Example with JavaScript

```javascript
// Example 1: Download the image directly
const downloadImage = async (imageFile) => {
  const form = new FormData();
  form.append("file", imageFile);

  const response = await fetch("http://your-api-url/remove-bg", {
    method: "POST",
    body: form,
  });

  const blob = await response.blob();
  // Create URL for the image blob
  const imageUrl = URL.createObjectURL(blob);
  // Use the image URL (e.g., display the image)
  const img = document.createElement("img");
  img.src = imageUrl;
  document.body.appendChild(img);
};

// Example 2: Upload to cloud storage using form data
const uploadToCloudWithFormData = async (
  imageFile,
  userId = "anonymous",
  filename = null
) => {
  const form = new FormData();
  form.append("file", imageFile);
  form.append("upload", "true");
  form.append("user_id", userId);
  if (filename) {
    form.append("filename", filename);
  }

  const response = await fetch("http://your-api-url/remove-bg", {
    method: "POST",
    body: form,
  });

  const result = await response.json();
  console.log("Uploaded image URL:", result.url);
  return result;
};

// Example 3: Upload to cloud storage using URL query parameters
const uploadToCloudWithQueryParams = async (
  imageFile,
  userId = "anonymous",
  filename = null
) => {
  const form = new FormData();
  form.append("file", imageFile);

  let url = `http://your-api-url/remove-bg?upload=true&user_id=${userId}`;
  if (filename) {
    url += `&filename=${encodeURIComponent(filename)}`;
  }

  const response = await fetch(url, {
    method: "POST",
    body: form,
  });

  const result = await response.json();
  console.log("Uploaded image URL:", result.url);
  return result;
};
```
