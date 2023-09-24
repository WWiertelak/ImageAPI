# ImageAPI Project

## Description
ImageAPI is a Django-driven platform designed to facilitate efficient management and sharing of images. With capabilities such as secure image uploads, expiring link generation, and efficient browsing of existing images.

## Features
**Secure Image Uploads:** Allows authenticated users to securely upload their images onto the platform.

**Thumbnail Generation:** Dynamically creates optimized thumbnails of uploaded images, tailored to user levels, enhancing the browsing experience and conserving bandwidth.

**Expiring Links:** Facilitates the creation of expiring links for images, ensuring limited time access and enhanced security.

**Image Browsing:** Provides users with an intuitive interface to easily navigate and browse available images, including their generated thumbnails, on the platform.

**Automated Tasks via Celery:** Employs Celery to run background processes that handle tasks such as thumbnail generation, obsolete thumbnail removal, and expired link deletion.

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
docker exec -it imageapi-web-1 python manage.py createsuperuser
```

### Loading Fixtures
To load initial data into the database:

Use the following commands:

```bash
docker exec -it imageapi-web-1 python manage.py loaddata /fixtures/imagesize_fixtures.json
docker exec -it imageapi-web-1 python manage.py loaddata /fixtures/userlevel_fixtures.json

```

## API Endpoints
Image Upload: Use the POST /upload/ endpoint to add images.

Generate Expiring Link: Generate time-limited access links with POST /create-expiring-link/.

Browse Available Images: Navigate through available images via GET /images/.



## Celery Tasks Overview
Within our application, we use Celery for asynchronous task processing. Here's a brief explanation of the tasks:

### Generate and Store Thumbnails:
```
generate_and_store_thumbnails()
```
Description: This function is responsible for creating thumbnails based on user levels. After generation, these thumbnails are stored in the database, and a dictionary containing links to them is returned. Simultaneously, the 'date_of_used' attribute for each thumbnail is updated to keep track of its most recent usage.

```
remove_old_thumbnails()
```
Description: Removes thumbnails that haven't been used for 30 days to optimize storage space.

```
remove_expired_links()
```
Description: Deletes links from the database that have expired. This ensures that old links do not consume unnecessary resources and that users cannot access images after a link's expiration.

