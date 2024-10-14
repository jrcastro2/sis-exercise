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

### Frontend (React)

After running the make command the frontend is available from here: http://localhost:3000/

## Notes

### Celery task

The celery task to harvest Inspire data can be run by executing:
```bash
    docker exec -it django_app python manage.py harvest_inspire_data
```

Please note that some data may not be ingested, and an error could be thrown in the Celery worker container due to validation issues. Most likely, this occurs because the publication date is missing. I used the current model as the source of truth and therefore enforced failure if it's missing.

### Search

Since the pagination is done on the backend it triggers a search every time we change page, increasing the user query count on that term. IMHO this is not the desired behaviour and should be addressed in the future.

### Other improvements

I have indexed the documents directly on a function of the "Document" class, ideally I would go for having a IndexerApi, able to abstract some logic like the bulk update, and reusable across other potential documents.

Also when working with conventional databases and search engines in combination I would be in favour of applying the Unit of Work pattern to ensure data consistency between both.

Thanks a lot for taking me into consideration for this job opportunity!