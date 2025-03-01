# Buggy AF

## Project Description
This project is a Python REST API built with FastAPI. The API allows for training machine learning models, saving them, and running inference.

## TODOs
- [ ] Set up a new Python project using Poetry
- [ ] Install FastAPI and Uvicorn
- [ ] Create the FastAPI app
- [ ] Implement endpoints for:
  - [ ] Training machine learning models
  - [ ] Saving trained models
  - [ ] Running inference on new data
- [ ] Add error handling and validation
- [ ] Write tests for the API endpoints
- [ ] Create documentation for the API

## Installation
1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Set up the project:
    ```sh
    poetry new buggy-af
    cd buggy-af
    ```

## Usage
1. Install dependencies:
    ```sh
    poetry install
    ```
2. Run the FastAPI app:
    ```sh
    poetry run uvicorn main:app --reload
    ```

## Endpoints
- `POST /train`: Train a new machine learning model
- `POST /save`: Save a trained model
- `POST /predict`: Run inference on new data

## Contributing
Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License.