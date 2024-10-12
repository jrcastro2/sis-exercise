# Assignment: INSPIREHEP Search & Summarization Web App

## Prerequisites

- Docker
- Docker-compose

## Setup

### Backend (Django)
1. Setup
    ```bash
        make up
        make bootstrap
        # visit localhost:8000
        # user: admin
        # password: admin
    ```

## Notes

The celery task to harvest Inspire data can be run by executing:
```bash
    docker exec -it django_app python manage.py harvest_inspire_data
```

Please note that some data may not be ingested, and an error could be thrown in the Celery worker container due to validation issues. Most likely, this occurs because the publication date is missing. I used the current model as the source of truth and therefore enforced failure if it's missing.