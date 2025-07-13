# CRUD-USER

A simple full-stack CRUD application for managing users, built with Flask for the backend and plain HTML/JavaScript for the frontend.

## Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```

2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Run the Flask application:
    ```bash
    python3 app.py
    ```
    The backend will be running at `http://127.0.0.1:5000`.

## Frontend Usage

Simply open the `frontend/index.html` file in your web browser. You can add and view users, which interacts with the running backend API.