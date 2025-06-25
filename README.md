# Fourth Dimensions API

A Flask REST API with Swagger documentation and admin panel for managing website content.

## Features

- RESTful API with Swagger documentation
- SQLite3 database for data storage
- File uploads for images and videos (paths stored in the database)
- Automatic URL generation for media files
- Admin panel for content management
- Authentication for secure access

## API Endpoints

The API provides endpoints for managing content in the following sections:

- Hero
- Interior
- Construction
- Property Consultancy
- About Us
- Our Team
- Testimonials
- Our Partners
- Why Us

## Media Handling

The API handles image and video uploads automatically:

1. When uploading media files through the API endpoints, the files are:
   - Saved to the appropriate directory (`static/uploads/images` or `static/uploads/videos`)
   - Given a unique filename to prevent collisions
   - The path is stored in the database
   - A URL is generated that can be used directly in templates

2. When retrieving media files through the API, each file includes:
   - `image_path` or `video_path`: The relative path to the file
   - `image_url` or `video_url`: The full URL that can be used directly in templates

3. Example of rendering media in templates:
   ```html
   <!-- For images -->
   <img src="{{ image.image_url }}" alt="{{ image.title }}">
   
   <!-- For videos -->
   <video controls>
       <source src="{{ video.video_url }}" type="video/mp4">
       Your browser does not support the video tag.
   </video>
   ```

4. Visit `/media-example` to see a demonstration of media rendering

## Setup and Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Fourth-dimensions-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Access the API documentation at:
   ```
   http://localhost:5000/api/docs
   ```

6. Access the admin panel at:
   ```
   http://localhost:5000/admin
   ```
   Default credentials:
   - Username: admin
   - Password: admin

## API Authentication

To access protected API endpoints, include the following header in your requests:
```
Authorization: admin-token
```

## Project Structure

```
Fourth-dimensions-api/
├── app/
│   ├── admin/            # Admin panel views
│   ├── api/              # API resources and schemas
│   │   ├── resources/    # API endpoints
│   │   └── schemas/      # Request/response schemas
│   ├── models/           # Database models
│   ├── static/           # Static files
│   │   └── uploads/      # Uploaded files
│   │       ├── images/   # Image uploads
│   │       └── videos/   # Video uploads
│   ├── templates/        # HTML templates
│   └── utils/            # Utility functions
├── migrations/           # Database migrations
├── app.py                # Application entry point
├── requirements.txt      # Dependencies
└── README.md             # This file
``` 