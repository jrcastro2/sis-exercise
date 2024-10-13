# Assignment: INSPIREHEP Search & Summarization Web App

## Prerequisites

- Docker
- Docker-compose
- Node.js version 20

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

### Frontend (React)

Please ensure that Node.js version 20 is installed. It’s recommended to use [nvm](https://github.com/nvm-sh/nvm) for managing Node versions.
Once Node.js is installed, navigate to the ui folder and install the necessary packages to run the application:
```bash
cd ui
npm install
npm start
# visit localhost:3000
```

## Notes

The celery task to harvest Inspire data can be run by executing:
```bash
    docker exec -it django_app python manage.py harvest_inspire_data
```

Please note that some data may not be ingested, and an error could be thrown in the Celery worker container due to validation issues. Most likely, this occurs because the publication date is missing. I used the current model as the source of truth and therefore enforced failure if it's missing.