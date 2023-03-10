## python-clean-architecture

#### Seba Ituarte - This structure will help in the project building using python and fastapi to isolate the dependencies and have a cleaner code

#### This api uses 3-layer Python - FastAPI Framework

![alt text](./fastapi.png)

### This app uses conventional commits

[Conventional commits url](https://www.conventionalcommits.org/en/v1.0.0/)

### Docker usage

    Build server
        docker-compose -p python-clean-architecture build
    
    Start server
        docker-compose up -d

    Stop server
        docker-compose down

### Standalone usage

    uvicorn app.main:app --reload

### Poetry usage

    Add a new dependency
        poetry add dependency_name / poetry add fastapi

    Install all dependencies in pyproject.toml
        poetry install

    To export dependecies into requirements.txt
        poetry export --without-hashes --format=requirements.txt > requirements.txt

### Testing

    To run unit testing
        python -m pytest app/tests/

    To run unit testing coverage
        python -m pytest --cov app/tests/

### Database migration script

    To run the script using alembic
        alembic upgrade head

### Environment variables

To modify/add configuration via environment variables, use the `.env` file, which contains basic app configuration.