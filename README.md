# ImageAPI Project

## Description
ImageAPI is a Django-based application for managing and sharing images. Users can upload images, generate expiring links for them, and browse available images.

## Features

- Image uploads by authenticated users.
- Generation of expiring links for images.
- Browsing of available images.
- Celery tasks for:
  - Generating and storing thumbnails based on user levels.
  - Removing old thumbnails that haven't been accessed in the last 30 days.
  - Deleting expired image links.

## Setup and Running

### Building Docker Images

```bash
docker-compose build
```
The application will be available at http://localhost:8000.

### Database Migrations
Run the database migrations in another terminal window with:

```bash
docker exec -it imageapi-web-1 python manage.py migrate
```

### Loading Fixtures
To load initial data into the database:

Use the following commands:

```bash
docker exec -it imageapi-web-1 python manage.py loaddata /fixtures/imagesize_fixtures.json
docker exec -it imageapi-web-1 python manage.py loaddata /fixtures/userlevel_fixtures.json

```

## API Documentation
Image Upload: POST /upload/

Generate Expiring Link: POST /create-expiring-link/

Browse Available Images: GET /images/


## Celery Tasks Overview
Within our application, we use Celery for asynchronous task processing. Here's a brief explanation of the tasks:

### Generate and Store Thumbnails:
```
generate_and_store_thumbnails()
```
Description: Generates thumbnails for a given image based on the user level and stores them in the database. Returns a dictionary of links to the generated thumbnails. It also updates the 'date_of_used' for each thumbnail.

```
remove_old_thumbnails()
```
Description: Removes thumbnails that haven't been used for 30 days to optimize storage space.

```
remove_expired_links()
```
Description: Deletes links from the database that have expired. This ensures that old links do not consume unnecessary resources and that users cannot access images after a link's expiration.

